"""
GuruDev story grabber
=====================
Downloads drawings from your Instagram story archive links, reframes them
(trims the empty story background), saves them to Libs/collections/<year>/,
and updates the Collections page + the year bar on the home page.

One-time setup
--------------
    pip install -r requirements.txt
    python -m playwright install chromium
    python stories.py login          # a browser opens: log in to Instagram, then close it

Everyday use
------------
    python stories.py add 2026 "Night Owl" https://www.instagram.com/stories/archive/1234567890/
        -> saves the link to Support/stories.json, downloads it, updates the site

    python stories.py                 # download every story in stories.json that has no image yet
    python stories.py --year 2025     # only one year
    python stories.py --only "Croc"   # only one name (any year)
    python stories.py --redo          # re-download even if the image already exists
    python stories.py --no-trim       # keep the full 9:16 story frame
    python stories.py pages           # just rebuild the Collections page from the folders

Your login is kept in the .ig-profile/ folder (ignored by git, never pushed).
"""
import argparse
import io
import json
import re
import sys
import time
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parent
STORIES_JSON = ROOT / "Support" / "stories.json"
COLLECTIONS = ROOT / "Libs" / "collections"
COLLECTIONS_PAGE = COLLECTIONS / "index.html"
HOME_PAGE = ROOT / "index.html"
PROFILE_DIR = ROOT / ".ig-profile"

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")


# ─── names ──────────────────────────────────────────────────────────────────
def clean_name(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "", name).strip()


def nice_title(stem: str) -> str:
    t = re.sub(r"[-_]+", " ", stem).strip()
    return t[:1].upper() + t[1:]


def find_existing(year_dir: Path, name: str):
    """Case-insensitive match so 'Cool-dog' finds 'cool-dog.jpg'."""
    want = clean_name(name).lower()
    if year_dir.is_dir():
        for f in year_dir.iterdir():
            if f.suffix.lower() in IMG_EXT and f.stem.lower() == want:
                return f
    return None


# ─── stories.json ───────────────────────────────────────────────────────────
def load_stories() -> dict:
    if STORIES_JSON.exists():
        return json.loads(STORIES_JSON.read_text(encoding="utf-8"))
    return {}


def save_stories(data: dict):
    STORIES_JSON.parent.mkdir(parents=True, exist_ok=True)
    data = {y: data[y] for y in sorted(data)}
    STORIES_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_duplicates(data: dict):
    seen = {}
    for y, items in data.items():
        for n, u in items.items():
            key = u.rstrip("/")
            if key in seen:
                print(f"  ! Same link used twice: {seen[key]} and {y}/{n} -> {u}")
            else:
                seen[key] = f"{y}/{n}"


# ─── reframing ──────────────────────────────────────────────────────────────
def reframe(img: Image.Image, trim=True) -> Image.Image:
    """Trim the flat story background around the drawing, keep a small margin."""
    img = img.convert("RGB")
    if not trim:
        return img
    w, h = img.size
    # background = median of the four corner patches
    p = max(4, w // 60)
    corners = [img.crop(b) for b in [(0, 0, p, p), (w - p, 0, w, p), (0, h - p, p, h), (w - p, h - p, w, h)]]
    px = sorted(sum((list(c.getdata()) for c in corners), []))
    bg = px[len(px) // 2]
    diff = ImageChops.difference(img, Image.new("RGB", img.size, bg)).convert("L")
    diff = diff.filter(ImageFilter.MedianFilter(5)).point(lambda v: 255 if v > 28 else 0)
    box = diff.getbbox()
    if not box:
        return img
    bw, bh = box[2] - box[0], box[3] - box[1]
    if bw * bh < 0.12 * w * h or bw * bh > 0.97 * w * h:
        return img  # nothing sensible to trim
    m = int(0.03 * max(bw, bh))
    box = (max(0, box[0] - m), max(0, box[1] - m), min(w, box[2] + m), min(h, box[3] + m))
    return img.crop(box)


def save_jpg(img: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if max(img.size) > 1600:
        img.thumbnail((1600, 1600), Image.LANCZOS)
    img.save(path, "JPEG", quality=92, optimize=True)


# ─── browser ────────────────────────────────────────────────────────────────
def open_browser(pw, headless=False):
    kw = dict(user_data_dir=str(PROFILE_DIR), headless=headless,
              viewport={"width": 1280, "height": 900}, device_scale_factor=2)
    try:
        return pw.chromium.launch_persistent_context(channel="chrome", **kw)
    except Exception:
        return pw.chromium.launch_persistent_context(**kw)


FIND_MEDIA_JS = """
() => {
  const vis = el => { const r = el.getBoundingClientRect();
    return r.width > 200 && r.height > 300 && r.bottom > 0 && r.top < innerHeight ? r.width * r.height : 0; };
  let best = null, area = 0;
  for (const el of document.querySelectorAll('video, img')) {
    const a = vis(el); if (a > area) { area = a; best = el; }
  }
  if (!best) return null;
  best.setAttribute('data-gd-story', '1');
  if (best.tagName === 'VIDEO') {
    return { kind: 'video', ready: best.readyState >= 2, duration: best.duration || 0 };
  }
  return { kind: 'img', ready: best.complete && best.naturalWidth > 0, src: best.currentSrc || best.src };
}
"""


def click_through_prompts(page):
    for label in ["View story", "View Story", "Allow all cookies", "Allow essential and optional cookies"]:
        try:
            b = page.get_by_role("button", name=label)
            if b.count():
                b.first.click(timeout=1500)
                time.sleep(0.8)
        except Exception:
            pass


def capture(page, url: str) -> Image.Image:
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    if "/accounts/login" in page.url:
        raise RuntimeError("Not logged in - run:  python stories.py login")
    click_through_prompts(page)

    media = None
    for _ in range(40):                       # up to ~20 s for the story to load
        media = page.evaluate(FIND_MEDIA_JS)
        if media and media["ready"]:
            break
        time.sleep(0.5)
    if not media:
        raise RuntimeError("Story did not load (link expired or not your archive?)")

    el = page.locator("[data-gd-story='1']").first

    if media["kind"] == "img":
        # pause the story timer, then fetch the full-resolution file with your session
        page.keyboard.press("Space")
        resp = page.request.get(media["src"])
        if resp.ok:
            return Image.open(io.BytesIO(resp.body()))
        return Image.open(io.BytesIO(el.screenshot()))

    # video story (e.g. a pan/zoom on the drawing): pause on a settled frame
    page.evaluate("""() => { const v = document.querySelector("[data-gd-story='1']");
        v.pause(); if (v.duration && isFinite(v.duration)) v.currentTime = v.duration * 0.85; }""")
    time.sleep(1.0)
    # try the native-resolution frame first; fall back to a hi-dpi screenshot
    data = page.evaluate("""() => { try {
        const v = document.querySelector("[data-gd-story='1']");
        const c = document.createElement('canvas'); c.width = v.videoWidth; c.height = v.videoHeight;
        c.getContext('2d').drawImage(v, 0, 0); return c.toDataURL('image/png'); } catch (e) { return null; } }""")
    if data:
        import base64
        return Image.open(io.BytesIO(base64.b64decode(data.split(",", 1)[1])))
    return Image.open(io.BytesIO(el.screenshot()))


# ─── page updates ───────────────────────────────────────────────────────────
def update_pages():
    years = sorted(int(d.name) for d in COLLECTIONS.iterdir()
                   if d.is_dir() and d.name.isdigit() and any(f.suffix.lower() in IMG_EXT for f in d.iterdir()))
    if not years:
        return
    html = COLLECTIONS_PAGE.read_text(encoding="utf-8")

    # keep existing year titles/descriptions and hand-written work titles
    old_meta, old_titles = {}, {}
    for m in re.finditer(r"(\d{4}):\s*\{\s*title:\s*'((?:[^'\\]|\\.)*)',\s*desc:\s*'((?:[^'\\]|\\.)*)'", html):
        old_meta[int(m.group(1))] = (m.group(2), m.group(3))
    for m in re.finditer(r"\{\s*src:\s*'([^']+)',\s*title:\s*'((?:[^'\\]|\\.)*)'\s*\}", html):
        old_titles[m.group(1).lower()] = m.group(2)

    stories = load_stories()
    json_titles = {}
    for y, items in stories.items():
        for n in items:
            json_titles[f"{y}/{clean_name(n)}".lower()] = n

    def esc(s):
        return s.replace("\\", "\\\\").replace("'", "\\'")

    blocks = []
    for y in years:
        title, desc = old_meta.get(y, (f"Works of {y}", "Ongoing."))
        files = sorted((f for f in (COLLECTIONS / str(y)).iterdir() if f.suffix.lower() in IMG_EXT),
                       key=lambda f: f.name.lower())
        rows = []
        for f in files:
            src = f"{y}/{f.name}"
            t = old_titles.get(src.lower()) or nice_title(json_titles.get(f"{y}/{f.stem}".lower(), f.stem))
            rows.append(f"          {{ src: '{esc(src)}', title: '{esc(t)}' }},")
        blocks.append(f"      {y}: {{\n        title:  '{esc(title)}',\n        desc:   '{esc(desc)}',\n"
                      f"        works:  [\n" + "\n".join(rows) + "\n        ]\n      }")

    new = (f"const YEARS = [{', '.join(map(str, years))}];\n\n    const YEAR_DATA = {{\n"
           + ",\n".join(blocks) + "\n    };\n\n    ")
    html2, n = re.subn(r"const YEARS = \[.*?\];\s*const YEAR_DATA = \{.*?\n    \};\s*", new, html, flags=re.S)
    if n != 1:
        print("  ! Could not find YEAR_DATA in Libs/collections/index.html - page not updated")
        return
    COLLECTIONS_PAGE.write_text(html2, encoding="utf-8")

    # home page year bar
    home = HOME_PAGE.read_text(encoding="utf-8")
    links = "\n".join(
        f'        <a href="Libs/collections/index.html?year={y}" target="_blank" class="yn-item">\n'
        f'          <span class="yn-year">{y}</span>\n        </a>' for y in years)
    home2, n = re.subn(r'(<div class="yn-scroll">\n).*?(\n      </div>)', lambda m: m.group(1) + links + m.group(2),
                       home, count=1, flags=re.S)
    if n == 1:
        HOME_PAGE.write_text(home2, encoding="utf-8")
    counts = ", ".join(f"{y}: {len([f for f in (COLLECTIONS / str(y)).iterdir() if f.suffix.lower() in IMG_EXT])}"
                       for y in years)
    print(f"Collections page updated ({counts})")


# ─── commands ───────────────────────────────────────────────────────────────
def cmd_login(_):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        ctx = open_browser(pw)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://www.instagram.com/accounts/login/")
        print("Log in to Instagram in the browser window, then close the window.")
        try:
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass
        ctx.close()
    print("Login saved.")


def cmd_sync(args, only_items=None):
    from playwright.sync_api import sync_playwright
    stories = load_stories()
    check_duplicates(stories)
    todo = []
    for y, items in sorted(stories.items()):
        if args.year and y != str(args.year):
            continue
        for name, url in items.items():
            if args.only and clean_name(name).lower() != clean_name(args.only).lower():
                continue
            if only_items is not None and (y, name) not in only_items:
                continue
            if not args.redo and find_existing(COLLECTIONS / y, name):
                continue
            todo.append((y, name, url))

    if not todo:
        print("Nothing to download - every story already has an image (use --redo to refresh).")
        update_pages()
        return

    print(f"{len(todo)} to download\n")
    ok, failed = 0, []
    with sync_playwright() as pw:
        ctx = open_browser(pw, headless=args.headless)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for i, (y, name, url) in enumerate(todo, 1):
            existing = find_existing(COLLECTIONS / y, name)
            out = existing.with_suffix(".jpg") if existing else COLLECTIONS / y / f"{clean_name(name)}.jpg"
            print(f"[{i}/{len(todo)}] {y}/{name} ...", end=" ", flush=True)
            try:
                img = reframe(capture(page, url), trim=not args.no_trim)
                save_jpg(img, out)
                print(f"saved {img.size[0]}x{img.size[1]}")
                ok += 1
            except Exception as e:
                print(f"FAILED - {e}")
                failed.append(f"{y}/{name}")
            time.sleep(1.5)  # be gentle with Instagram
        ctx.close()

    print(f"\nDone: {ok} saved, {len(failed)} failed")
    if failed:
        print("Failed: " + ", ".join(failed) + "\nRun the same command again to retry just these.")
    update_pages()


def cmd_add(args):
    if not re.match(r"https://(www\.)?instagram\.com/stories/", args.url):
        sys.exit("That doesn't look like an Instagram story link.")
    stories = load_stories()
    stories.setdefault(str(args.year), {})[args.name] = args.url
    save_stories(stories)
    print(f"Added {args.year}/{args.name} to stories.json")
    args.redo, args.only, args.year = True, None, None
    cmd_sync(args, only_items={(str(args.add_year), args.name)})


def main():
    ap = argparse.ArgumentParser(description="Download & reframe drawings from Instagram story links.")
    ap.add_argument("command", nargs="?", default="sync", choices=["sync", "login", "add", "pages"])
    ap.add_argument("rest", nargs="*", help='for add:  YEAR "Name" URL')
    ap.add_argument("--year")
    ap.add_argument("--only")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--no-trim", action="store_true")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()

    if args.command == "login":
        cmd_login(args)
    elif args.command == "pages":
        update_pages()
    elif args.command == "add":
        if len(args.rest) != 3:
            sys.exit('Usage: python stories.py add YEAR "Name" URL')
        args.add_year, args.name, args.url = args.rest
        args.year = args.add_year
        cmd_add(args)
    else:
        cmd_sync(args)


if __name__ == "__main__":
    main()
