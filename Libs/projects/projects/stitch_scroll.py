"""
Scroll stitcher v8
- Rotation: CW for sheets 1-3, CCW for sheets 9-10
- Coarse crop (warm_thresh=0.10) removes bulk table
- whiten_table() replaces residual orange pixels with white (preserves A4 ratio)
  bottom band widened to 25% (table is deeper than top/left/right)
- min-width 82%, A4 ratio enforced
- Per-sheet brightness normalisation
- ORB overlap detection (max 150px), seam equalisation (zone=100px)
"""

import os
import numpy as np
from PIL import Image
import cv2

SCROLL_DIR   = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll project"
OUTPUT_FILE  = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll_stitched.jpg"
PREVIEW_FILE = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll_preview.jpg"

FILES = [
    'Media.jpg',     # 1
    'Media (1).jpg', # 2
    'Media (2).jpg', # 3
    'Media (3).jpg', # 4
    'Media (4).jpg', # 5
    'Media (5).jpg', # 6
    'Media (6).jpg', # 7
    'Media (7).jpg', # 8
    'Media (8).jpg', # 9
    'Media (9).jpg', # 10
]

ROTATIONS = [-90, -90, -90, 0, 0, 0, 0, 0, 90, 90]
A4_RATIO  = 297.0 / 210.0   # = 1.4143


# ─── colour helpers ───────────────────────────────────────

def _hsv(img_rgb):
    bgr = img_rgb[:, :, ::-1].copy()
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(float)   # H:0-180 S V:0-255

def paper_mask(img_rgb):
    hsv = _hsv(img_rgb)
    return (hsv[:,:,2] > 185) & (hsv[:,:,1] < 82)

def warm_mask_broad(img_rgb):
    """Orange-brown table (broad, for coarse crop)."""
    h, s, v = _hsv(img_rgb)[:,:,0], _hsv(img_rgb)[:,:,1], _hsv(img_rgb)[:,:,2]
    return (h >= 5) & (h <= 30) & (s > 50) & (v > 60) & (v < 242)

def warm_mask_narrow(img_rgb):
    """
    Narrower table mask (for whitening residual pixels).
    Avoids gold/yellow drawing elements which have H > 18 and high saturation.
    """
    hsv = _hsv(img_rgb)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    # Brown-orange only: lower H (not yellow), moderate S (not vivid gold), medium V
    return (h >= 4) & (h <= 18) & (s > 40) & (s < 175) & (v > 55) & (v < 215)


# ─── 1. Coarse crop ───────────────────────────────────────

def coarse_crop(img_rgb, label=''):
    h, w = img_rgb.shape[:2]
    pm  = paper_mask(img_rgb).astype(float)
    wm  = warm_mask_broad(img_rgb).astype(float)
    rp, rw = pm.mean(axis=1), wm.mean(axis=1)
    cp, cw = pm.mean(axis=0), wm.mean(axis=0)

    PT, WT, C = 0.38, 0.10, 2    # paper thresh, warm thresh, consecutive rows needed

    def first_ok(rp, rw):
        cnt = 0
        for i in range(len(rp)):
            cnt = cnt+1 if (rp[i] >= PT and rw[i] < WT) else 0
            if cnt >= C: return max(0, i-C+1)
        return 0

    def last_ok(rp, rw):
        cnt = 0
        for i in range(len(rp)-1, -1, -1):
            cnt = cnt+1 if (rp[i] >= PT and rw[i] < WT) else 0
            if cnt >= C: return min(len(rp)-1, i+C-1)
        return len(rp)-1

    top, bot  = first_ok(rp, rw), last_ok(rp, rw)
    lft, rgt  = first_ok(cp, cw), last_ok(cp, cw)

    # Min width = 82% of image (keeps sheet-10 scale consistent)
    mw = int(0.82 * w)
    if rgt - lft + 1 < mw:
        deficit = mw - (rgt - lft + 1)
        al = deficit // 2;  ar = deficit - al
        nl = max(0, lft-al);   nr = min(w-1, rgt+ar)
        if nl == 0:   nr = min(w-1, nr + (al-lft))
        if nr == w-1: nl = max(0, nl - (ar-(w-1-rgt)))
        lft, rgt = nl, nr

    # A4 ratio enforcement (keep width, adjust height symmetrically)
    cw2   = rgt - lft + 1
    exp_h = int(round(cw2 / A4_RATIO))
    ch    = bot - top + 1
    if abs(ch - exp_h) > 12:
        dt  = exp_h - ch
        top = max(0,   top - dt//2)
        bot = min(h-1, bot + (dt - dt//2))

    out = img_rgb[top:bot+1, lft:rgt+1]
    r   = out.shape[1] / max(out.shape[0], 1)
    print(f'  {label}: ({lft},{top})->({rgt},{bot})  {out.shape[1]}x{out.shape[0]}  r={r:.3f}')
    return out


# ─── 2. Whiten residual table pixels ──────────────────────

def whiten_table(img_rgb):
    """
    Replace narrowly-defined table-coloured pixels with white.
    This eliminates the orange strip without changing image dimensions
    or touching gold/coloured drawing elements.
    """
    mask = warm_mask_narrow(img_rgb)
    # Only apply within the outer 12% of the image (edges near table)
    h, w = img_rgb.shape[:2]
    edge_mask = np.zeros((h, w), bool)
    t12h = int(0.12 * h);  t25h = int(0.25 * h);  t12w = int(0.12 * w)
    edge_mask[:t12h,  :] = True    # top band (12%)
    edge_mask[-t25h:, :] = True    # bottom band (25% - table is deeper here)
    edge_mask[:, :t12w]  = True    # left band
    edge_mask[:, -t12w:] = True    # right band

    apply = mask & edge_mask
    out = img_rgb.copy()
    out[apply] = 248     # replace with near-white
    n = apply.sum()
    if n > 0:
        print(f'    whiten: {n} px replaced')
    return out


# ─── 3. Brightness normalisation ──────────────────────────

def norm_bright(img_rgb):
    gray  = img_rgb.astype(float).mean(axis=2)
    white = np.percentile(gray, 97)
    if white < 10: return img_rgb
    return np.clip(img_rgb.astype(float) * (248.0/white), 0, 255).astype(np.uint8)


# ─── 4. Overlap detection ─────────────────────────────────

def find_overlap(right_img, left_img, max_s=150):
    h  = min(right_img.shape[0], left_img.shape[0])
    mg = h // 5
    g1 = cv2.cvtColor(right_img[mg:h-mg, -max_s:], cv2.COLOR_RGB2GRAY)
    g2 = cv2.cvtColor(left_img [mg:h-mg, :max_s],  cv2.COLOR_RGB2GRAY)
    orb = cv2.ORB_create(nfeatures=4000)
    k1, d1 = orb.detectAndCompute(g1, None)
    k2, d2 = orb.detectAndCompute(g2, None)
    if d1 is None or d2 is None or len(d1)<8 or len(d2)<8: return 0
    bf   = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    raw  = sorted(bf.match(d1, d2), key=lambda m: m.distance)
    good = [m for m in raw[:60] if m.distance < 45]
    if len(good) < 6: return 0
    cands = [max_s - k1[m.queryIdx].pt[0] + k2[m.trainIdx].pt[0] for m in good]
    cands = [c for c in cands if 5 < c < max_s-5]
    if len(cands) < 4: return 0
    med = float(np.median(cands))
    inl = [c for c in cands if abs(c-med) < 15]
    if len(inl) < 4: return 0
    ov = int(round(np.median(inl)))
    print(f'  overlap: {ov}px ({len(inl)} matches)')
    return ov


# ─── 5. Seam brightness equalisation ──────────────────────

def equalise_seam(canvas, sx, zone=100):
    x0 = max(0, sx-35)
    lm = canvas[:, x0:sx].astype(float).mean()
    rm = canvas[:, sx:min(canvas.shape[1], sx+35)].astype(float).mean()
    if rm < 5 or lm < 5: return
    corr = lm / rm
    if abs(corr-1.0) > 0.40: return
    x3 = min(canvas.shape[1]-1, sx+zone)
    n  = x3 - sx + 1
    for i, x in enumerate(range(sx, x3+1)):
        t = i/(n-1) if n>1 else 1.0
        f = corr*(1-t) + 1.0*t
        canvas[:, x] = np.clip(canvas[:, x].astype(float)*f, 0, 255).astype(np.uint8)


# ─── Main ─────────────────────────────────────────────────

def main():
    sheets = []
    print('=== Step 1: Load / Rotate / Crop / Whiten ===')
    for i, (fname, rot) in enumerate(zip(FILES, ROTATIONS)):
        path = os.path.join(SCROLL_DIR, fname)
        print(f'\nSheet {i+1}: {fname}')
        img = Image.open(path).convert('RGB')
        if rot != 0:
            img = img.rotate(rot, expand=True)
            print(f'  Rotated {"CW" if rot<0 else "CCW"} -> {img.width}x{img.height}')
        arr    = np.array(img)
        arr    = coarse_crop(arr, label=f's{i+1}')
        arr    = whiten_table(arr)
        arr    = norm_bright(arr)
        sheets.append(arr)

    print('\n=== Step 2: Normalise height ===')
    heights  = [s.shape[0] for s in sheets]
    target_h = int(np.median(heights))
    print(f'target_h={target_h}  per-sheet={heights}')

    normed = []
    for i, s in enumerate(sheets):
        h, w  = s.shape[:2]
        nw    = int(round(w * target_h / h))
        r     = cv2.resize(s, (nw, target_h), interpolation=cv2.INTER_LANCZOS4)
        normed.append(r)
        print(f'  s{i+1}: {w}x{h} -> {nw}x{target_h}  ratio={nw/target_h:.3f}')

    print('\n=== Step 3: Stitch ===')
    result = normed[0].copy()
    seams  = []
    for i in range(1, len(normed)):
        print(f'Sheet {i+1}:')
        ov     = find_overlap(result, normed[i])
        nxt    = normed[i][:, ov:] if ov > 0 else normed[i]
        sx     = result.shape[1]
        result = np.concatenate([result, nxt], axis=1)
        seams.append(sx)
        print(f'  width={result.shape[1]}')

    print('Equalising seams ...')
    result = result.copy()
    for sx in seams:
        equalise_seam(result, sx)

    print(f'\nFinal: {result.shape[1]} x {result.shape[0]} px')
    Image.fromarray(result).save(OUTPUT_FILE, 'JPEG', quality=95)
    print(f'Saved: {OUTPUT_FILE}')
    pw = min(4000, result.shape[1])
    ph = int(result.shape[0] * pw / result.shape[1])
    prev = cv2.resize(result, (pw, ph), interpolation=cv2.INTER_AREA)
    Image.fromarray(prev).save(PREVIEW_FILE, 'JPEG', quality=92)
    print(f'Preview: {PREVIEW_FILE}')


if __name__ == '__main__':
    main()
