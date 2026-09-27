# NINE LIVES website

- `index.html`: the whole page (CSS and JS inline): the logo, the pitch with the cat rising out of its bottom line,
  the features, screenshots, download, and the title screen's burning skyline as the footer.
- `img/`: everything it shows, made by `python3 make_site.py` (~20 s): the logo, the cat with his guns, the
  skyline, the badge and the tab icon are drawn by `../art/gen.py` and dithered by `../art/dither.html`, so they match the
  game's title screen; the screenshots are copied from `../shots/selftest` (list and captions: `SHOTS_USED`).
  `python3 make_site.py logo shots` redoes only those.
- `lo/`: the renderer's scratch files (not backed up, not published).

## The download link

The button says COMING SOON until its `href` (search index.html for `id="dl"`) changes from `#download` to the
file's URL. Update the size in the button and the DISK SPACE row if the build shrinks.

Package the app with `ditto -c -k --sequesterRsrc --keepParent "NINE LIVES.app" NINE-LIVES-mac.zip` (keeps its
signature). The data is already Oodle-compressed, so the zip is nearly as big as the app.

## Hosting

- The page: https://9lives.millertechnology.net, GitHub Pages from `main` of github.com/bigmillz/ninelives-site
  (this folder; `CNAME` holds the domain). To update: `git commit -am "..." && git push`; live in about a minute.
  DNS: a Cloudflare CNAME `9lives` -> `bigmillz.github.io`, DNS only (grey cloud) so GitHub can issue HTTPS.
- The download: too big for GitHub (2 GiB per release file) or itch.io (2 GB by default, 4 GB on request).
  Plan: a Cloudflare R2 bucket on a millertechnology.net subdomain. R2 charges nothing for downloads; storage
  is free to 10 GB, then $0.015 per GB-month (18 GB is about $0.12 a month). Upload with rclone (multipart);
  the dashboard and wrangler cap single uploads at ~300 MB.
