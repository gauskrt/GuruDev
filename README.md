# GuruDev — Art Portfolio

Bright · Editorial · Paper & Ink aesthetic.

---

## Folder Structure

```
art/
├── index.html                  ← Main portfolio page
├── exhibitions/
│   └── index.html              ← Exhibition pages (one URL, data-driven)
├── collections/
│   └── index.html              ← Year collections archive
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── logo.png                ← Your logo (drop in here to replace text)
│   ├── doodles/                ← Background SVG doodles
│   └── Libs/
│       ├── about/              ← Hero carousel BGs + avatar photo
│       ├── notable projects/   ← Individual standout pieces
│       ├── carousel/           ← Images for the scrolling strips (optional)
│       ├── exhibitions/        ← One sub-folder per exhibition
│       └── projects/
│           ├── scroll project/ ← Panoramic scroll image
│           ├── daily project/  ← Project 52 weekly images
│           └── collections/    ← Year sub-folders (2023/, 2024/ …)
└── README.md
```

---

## Logo

Drop your logo file into `images/logo.png` (PNG, SVG, or JPG all work). The nav will automatically display it. If the file is missing, the text "GuruDev" shows as a fallback.

---

## Quick Start: Drop In Your Images

### `images/Libs/about/`
| Filename | What it's for |
|----------|--------------|
| `bg-1.jpg` | Hero section background carousel |
| `bg-2.jpg` | Counter section background |
| `bg-3.jpg` | Inspiration section background |
| `avatar.jpg` | Your portrait photo (3:4 ratio works best) |

### `images/Libs/notable projects/`
Files: `work-1.jpg` → `work-9.jpg` (and beyond)

To add a new card: copy a `.nw-card` block in `index.html` and update `src`, `alt`, number and title. All cards are uniform squares — no size class needed.

### `images/Libs/carousel/`
Images for the two scrolling strips below the counter. Drop any number of images here, then update `CAROUSEL_IMAGES` in `js/main.js` with the file paths.

---

## Adding / Editing Exhibitions

Exhibitions appear in the **Exhibitions** dropdown in the main nav. Each item links to `exhibitions/index.html?id=your-id`.

### Step 1 — Add images
Create a folder: `images/Libs/exhibitions/your-exhibition-id/`
Drop your artwork files in there as `work-01.jpg`, `work-02.jpg`, etc.

### Step 2 — Register the exhibition
Open `exhibitions/index.html` and find the `EXHIBITIONS` object. Add a new entry:

```js
'your-exhibition-id': {
  title:  'Exhibition Title',
  desc:   'A short description shown in the hero.',
  date:   '2025',           // shown as a subtitle label
  heroId: 'EX',             // 2–3 decorative letters in the hero
  works: [
    { src: '../images/Libs/exhibitions/your-exhibition-id/work-01.jpg', title: 'Work Title' },
    { src: '../images/Libs/exhibitions/your-exhibition-id/work-02.jpg', title: 'Work Title' },
    // add as many as you like
  ]
},
```

### Step 3 — Add the nav link
Open `index.html` and find the `EXHIBITIONS DROPDOWN` comment inside `<nav id="navbar">`. Add a line:

```html
<a href="exhibitions/index.html?id=your-exhibition-id" class="nav-dd-item">Exhibition Name</a>
```

That's it — the page builds itself from the data.

---

## In Your Space (room mockups)

Section 03 shows the art hanging in four CSS-drawn rooms: living room, bedroom, study and café/lobby.
They need no photos or licences and scale with the screen.

- To change the art in a room, edit the `<img src>` inside that room's `.art` frame in `index.html`.
- Each frame has `data-shape="square"` or `data-shape="portrait"` (4:5). The **Try another piece** button
  cycles through `ROOM_ART` in `js/main.js`; add new pieces to the right list there.
- To move or resize a frame, change its inline `style="--w:21%; left:50%; top:7%;"`.

## Prints & Originals (quote only)

Section 04 has no prices. Every button opens an Instagram DM (`ig.me/m/artbygurudev`) or a pre-filled email
to `artbygurudev@gmail.com`. Put images of available works in `Libs/projects/For Sale/Originals/` and
`Libs/projects/For Sale/Prints/`.

## Rights & Usage

The intellectual-property notice is the `#rights` section just above the footer. The footer of every page links to it.

---

## Downloading drawings from Instagram stories (`stories.py`)

`stories.py` downloads each story at full resolution, crops away the empty story background,
saves it to `Libs/collections/<year>/<Name>.jpg`, and updates the Collections page and the year bar.
The story links live in `Support/stories.json`.

```bash
pip install -r requirements.txt
python -m playwright install chromium
python stories.py login                       # one time: log in to Instagram, then close the window

python stories.py add 2026 "Night Owl" https://www.instagram.com/stories/archive/1234567890/
python stories.py                             # fetch every story in stories.json that has no image yet
python stories.py --redo --year 2022          # re-download a year (e.g. to replace old low-res captures)
python stories.py --only "Croc" --no-trim     # one story, keep the full 9:16 frame
python stories.py pages                       # only rebuild the Collections page from the folders
```

Your login stays in `.ig-profile/`, which git ignores.

---

## Dark Mode

Click the **◐** button in the top-right of the nav. The preference is saved in `localStorage` and persists across visits.

---

## Counter Start Date

In `js/main.js`, find:
```js
const START_DATE = new Date('2022-01-06');
```
Change to the date you started drawing consistently.

---

## Social Links & Email

In `index.html`, find the `<footer>` section:
- Instagram is set to `@artbygurudev`
- YouTube and X/Twitter are commented out — uncomment to re-enable
- Update `href="mailto:hello@gurudev.art"` with your actual email

---

## Customising Text

All placeholder text is in `index.html`. Key elements to edit:

| Section | Element |
|---------|---------|
| Hero tagline | `<p class="hero-tagline">` |
| About me card | `<p>` inside `.about-card` |
| Counter caption | `<p class="counter-desc">` |
| Inspiration heading + body | `.inspire-heading` + `.inspire-body` |
| Scroll Project caption | `<p>` inside `.sp-text-float` |
| Project 52 subheading | `<p class="p52-subhead">` |
| Footer tagline | `<p class="footer-tagline">` |

---

## Year Collections Archive

Open `collections/index.html` and find `YEAR_DATA`. Add image entries to any year:

```js
2025: {
  title: 'Present Tense',
  desc:  'Ongoing.',
  works: [
    { src: '../images/Libs/projects/collections/2025/work-01.jpg', title: 'Session 01' },
  ]
}
```

---

## Colour Changes

All design tokens are in `css/style.css` inside `:root {}`:

| Variable | Default | Role |
|----------|---------|------|
| `--signal` | `#e05a2b` | Coral accent — borders, labels, numbers |
| `--flare`  | `#2563eb` | Blue — secondary accent |
| `--void`   | `#f8f3ed` | Page background (warm off-white) |
| `--cream`  | `#17110d` | Headings |
| `--bone`   | `#2e2622` | Body text |

Dark mode overrides these under `[data-theme="dark"]` in `css/style.css`.

---

## Fonts (loaded from Google Fonts)
- **Cormorant Garamond** — serif, headings and body
- **Syne** — bold sans-serif, section numbers
- **DM Mono** — monospace, labels and captions
- **Kaushan Script** — logo / brand name

---

## GitHub Pages Deploy
Push the entire folder contents as the root of your repository, or set GitHub Pages source to the root of `main`. The `_config.yml` disables Jekyll so plain HTML is served as-is.
