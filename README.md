# Intuitive Information

Source for the *Intuitive Information* blog: one folder per post, Markdown with YAML front
matter, so it can be published to any static site generator (Hugo, Astro, Jekyll, ...) or
pasted into a hosted platform.

```
posts/<date>-<slug>/
  index.md      the post (front matter: title, date, draft, series, tags)
  figures/      images and GIFs, linked relatively from index.md
  source/       SVG originals and the scripts that generate the figures
  original.pdf  (part 1 only) the 2013 Word export the post was transcribed from
```

## Posts

| Date | Post | Status |
| --- | --- | --- |
| 2013-04-01 | Catching a cheater with a cube: Hamming codes on the hypercube (part 1) | published; proofread, figures redrawn (5 figures, 3 GIFs), unfinished ending completed |
| 2026-10-08 | Catching three cheaters with a tesseract: Reed–Muller codes on the hypercube (part 2) | published; reconstruction of the lost 2013 sequel |

Part 2 explains only the original 2013 ECC-HyperCube algorithm (github.com/bomot113/ECC-HyperCube).
Later optimizations belong in a separate post.

## Regenerating part 1's figures

From `posts/2013-04-01-hamming-hypercube/source/`: `p1fig1.py`, `p1cube_figs.py`, `p1hyper_figs.py`
write the SVGs (and the cube GIF's frames); `p1tess_gifs.py` writes the tesseract GIF frames from
the 2013 one-error test vectors. Render and assemble the same way as part 2.

## Regenerating part 2's figures

From `posts/2026-10-08-hamming-hypercube-part-2/source/`:

```sh
python3 fig1.py && python3 fig2_6.py && python3 fig7_8.py && python3 fig9.py   # write SVGs
./render.sh fig1 1240 760                                                     # SVG -> PNG via headless Chrome (2x)
python3 gif_encode.py && python3 detect_gif.py                                # GIF frames (SVG)
```

GIF frames are rendered with headless Chrome at 1x and assembled with Pillow
(`~/miniconda3/bin/python`). `trace.py` and `trace2.py` replay the 2013 decoder step by step
on the example words; `search2.py` found the cube-in-cube layout.

## Site

Built with Hugo (`hugo.toml`, `layouts/`, `static/style.css`; `posts/` is mounted as the content
section, `source/` folders are not published) and deployed to tuebui.com on every push to `main`
(see Hosting on AWS below). Preview locally with `hugo server`.
New posts go in `posts/<date>-<slug>/index.md` with `slug:`, `description:` (shown on the front page)
and, for a series, `series:` and `part:` in the front matter, plus a `cover.svg` for the front-page card.
`tools/art.py` regenerates the hero tesseract (`layouts/_partials/tesseract.html`) and both covers.

## Hosting on AWS (tuebui.com)

`infra/site.yaml` (CloudFormation, us-east-1) creates the private S3 bucket, the CloudFront
distribution with its certificate, the Route 53 records for `tuebui.com` and `www`, and a
GitHub Actions role limited to this repo's `main` branch. `.github/workflows/deploy-aws.yml`
builds the site, syncs it to the bucket and invalidates the CloudFront cache. It runs once the
repository variables `AWS_ROLE_ARN`, `S3_BUCKET` and `CLOUDFRONT_DISTRIBUTION_ID` are set
from the stack's outputs.
