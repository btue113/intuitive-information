# Intuitive Information

Source for the *Intuitive Information* blog: one folder per post, Markdown with YAML front
matter, so it can be published to any static site generator (Hugo, Astro, Jekyll, ...) or
pasted into a hosted platform.

```
posts/<date>-<slug>/
  index.md      the post (front matter: title, date, draft, series, tags)
  figures/      images and GIFs, linked relatively from index.md
  source/       SVG originals and the scripts that generate the figures
  original.pdf  (part 1 only) the 2013 Word export the text was transcribed from
```

## Posts

| Date | Post | Status |
| --- | --- | --- |
| 2013-04-01 | Just another generalized version of Hamming Code – Hypercube representation | transcribed from the PDF; figures still to export from the Word file in OneDrive |
| 2026-10-08 | Part 2 – Reed–Muller codes on the hypercube | draft; reconstruction of the lost 2013 sequel |

Part 2 explains only the original 2013 ECC-HyperCube algorithm (github.com/bomot113/ECC-HyperCube).
Later optimizations belong in a separate post.

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
