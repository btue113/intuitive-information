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
| 2013-04-01 | Catching a cheater with a cube: Hamming codes on the hypercube (part 1) | draft; proofread, figures redrawn (5 figures, 3 GIFs), unfinished ending completed |
| 2026-10-08 | Catching three cheaters with a tesseract: Reed–Muller codes on the hypercube (part 2) | draft; reconstruction of the lost 2013 sequel |

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
