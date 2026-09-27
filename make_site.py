"""NINE LIVES website art: the logo, the cat with his guns, the skyline and the badges, drawn with the
game's own title-screen code (art/gen.py) and dithered the same way (art/dither.html), plus the chosen
self-test screenshots as JPEGs. Run: python3 make_site.py  ->  img/*
The page itself is index.html (hand-written); this only makes what it shows.
"""
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(os.path.dirname(HERE), "art")
SHOTS = os.path.join(os.path.dirname(HERE), "shots", "selftest")
IMG = os.path.join(HERE, "img")
LO = os.path.join(HERE, "lo")
sys.path.insert(0, ART)
import gen  # noqa: E402  (the title screen's SVG pieces: logo, cat, skyline, fire, badge, label)
from PIL import Image  # noqa: E402

os.makedirs(os.path.join(IMG, "shots"), exist_ok=True)
os.makedirs(LO, exist_ok=True)

# Screenshots on the page, in order: file in shots/selftest, caption in the HUD's own words.
SHOTS_USED = [
    ("13_hood_clear", "HOOD CLEAR  //  MYRTLE & STOCKHOLM"),
    ("08_knickerbocker", "THAMES & KNICKERBOCKER  //  11:16 PM"),
    ("26_grenade_glow", "TROUTMAN & WYCKOFF  //  HE WANTS YOUR PARKING SPOT"),
    ("06d_grenade", "DEKALB & IRVING  //  TWO DEAGLES"),
    ("18_trash", "DEKALB & KNICKERBOCKER  //  TRASH BAG"),
    ("24_corner", "STARR & KNICKERBOCKER  //  11:40 PM"),
    ("19b_laser", "THE UNTER LASER  //  A HOOD CLEAR PAYS"),
    ("17a_empty", "DEKALB & IRVING  //  SMOKE BREAK"),
    ("09c_map_late", "TAB  //  ALL 147 BLOCKS"),
]


def logo_text():
    """NINE LIVES and the ON KNICKERBOCKER banner alone, as on the title screen (same size and glow)."""
    return gen.page(400, 140, gen.logo(200, 84, 64, sub=True, sub_size=17))


def logo_burst():
    """The standalone logo: the title's burst behind the lockup."""
    b = ['<polygon points="%s" fill="url(#boom)" opacity="0.9"/>' % gen.star(240, 160, 24, 158, 50, random.Random(21), 0.18)]
    b.append('<circle cx="240" cy="160" r="62" fill="url(#boom)" filter="url(#blur6)"/>')
    b.append(gen.logo(240, 150, 64, sub=True, sub_size=17))
    return gen.page(480, 320, "\n".join(b))


def skyline_strip():
    """The foot of the title screen (row houses and fire), sky left transparent, to close the page."""
    b = [gen.skyline(random.Random(17), 70), gen.fire(34, 80)]
    return gen.page(640, 114, "\n".join(b))


def cat_guns():
    """The title screen's cat with his two gold Deagles, cut flat at the hoodie (y 190) so he can rise out of a line."""
    return gen.page(250, 298, gen.cat(125, 108, 1.0, guns=True))


def cat_icon():
    """The cat's head in its shades on the night sky: the tab icon and the home-screen icon."""
    b = ['<rect width="180" height="180" fill="url(#sky)"/>', gen.cat(90, 118, 0.98, guns=False)]
    return gen.page(180, 180, "\n".join(b))


def render(name, html, w, h, scale, colors, scan):
    """gen.render, but into img/ (art/out is copied into the game)."""
    src = os.path.join(LO, name + ".html")
    open(src, "w").write(html)
    lo_png = os.path.join(LO, name + ".png")
    gen.chrome_shot(src, lo_png, w, h)
    if scale == 0:   # no dither: straight render
        shutil.copy(lo_png, os.path.join(IMG, name + ".png"))
        return
    q = "src=%s&scale=%d&colors=%d&scan=%d" % (lo_png, scale, colors, 1 if scan else 0)
    out_png = os.path.join(IMG, name + ".png")
    subprocess.run([gen.CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", "--default-background-color=00000000",
                    "--virtual-time-budget=8000", "--window-size=%d,%d" % (w * scale, h * scale),
                    "--screenshot=%s" % out_png, "file://%s/dither.html?%s" % (ART, q)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # dithered art has at most a couple hundred colours: store it as a palette PNG (a fraction of the size)
    im = Image.open(out_png).convert("RGBA")
    if len(im.getcolors(1 << 16) or []) <= 256:
        im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(out_png, optimize=True)
    print("wrote", out_png)


def shots():
    for name, _ in SHOTS_USED:
        im = Image.open(os.path.join(SHOTS, name + ".png")).convert("RGB")
        im.save(os.path.join(IMG, "shots", name + ".jpg"), quality=84, optimize=True, progressive=True)
        im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(
            os.path.join(IMG, "shots", name + "_t.jpg"), quality=82, optimize=True, progressive=True)
    print("wrote %d screenshots" % len(SHOTS_USED))


def icons():
    src = Image.open(os.path.join(IMG, "cat_icon.png")).convert("RGB")
    src.save(os.path.join(IMG, "apple-touch-icon.png"))
    src.resize((64, 64), Image.LANCZOS).save(os.path.join(IMG, "favicon.png"))
    os.remove(os.path.join(IMG, "cat_icon.png"))
    # the link-preview card: the real title screen, cropped to 1200 x 630
    menu = Image.open(os.path.join(ART, "out", "menu.png")).convert("RGB").resize((1200, 675), Image.LANCZOS)
    menu.crop((0, 0, 1200, 630)).save(os.path.join(IMG, "og.jpg"), quality=86, optimize=True)
    print("wrote icons, og card")


if __name__ == "__main__":
    only = sys.argv[1:]
    jobs = [("logo_text", logo_text(), 400, 140, 3, 48, False),
            ("logo", logo_burst(), 480, 320, 3, 64, False),
            ("skyline", skyline_strip(), 640, 114, 3, 64, False),
            ("cat_guns", cat_guns(), 250, 298, 3, 64, False),
            ("badge_meow", gen.page(120, 120, gen.badge(60, 60, 50, ["RATED M", "FOR", "MEOW"], rot=-12)), 120, 120, 3, 16, False),
            ("cat_icon", cat_icon(), 180, 180, 0, 0, False)]
    for j in jobs:
        if not only or j[0] in only:
            render(*j)
    if not only or "cat_icon" in only:
        icons()
    if not only or "shots" in only:
        shots()
