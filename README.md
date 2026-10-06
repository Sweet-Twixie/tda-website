# Shape of Data

A Quarto website for a TDA blog, course and article database.

## Run it on your computer

1. Install Quarto: https://quarto.org/docs/get-started/
2. In this folder run:

   ```bash
   quarto preview
   ```

   The site opens in your browser and refreshes every time you save a file.

To run the Python notebooks:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

then set `eval: true` at the top of the notebook page.

## Put it online (GitHub Pages, free)

1. Create a repo called `tda-website` on GitHub and push this folder to it.
2. Run once from this folder: `quarto publish gh-pages`
   (creates the `gh-pages` branch and publishes the site).
3. In the repo go to **Settings → Pages** and check the source is the `gh-pages` branch.
4. From then on, every push to `main` republishes automatically (`.github/workflows/publish.yml`).
   Commit the `_freeze/` folder so notebook outputs don't need re-running on GitHub.

## Where to change things

| I want to change… | File |
|---|---|
| Colours, fonts, text size | `theme.scss` (top block) |
| Any other styling | `theme.scss` (below `scss:rules`) |
| Navbar links, sidebar course structure, footer | `_quarto.yml` |
| Landing page text and barcode picture | `index.qmd` |
| Add a lesson | create a `.qmd` in `course/…`, then list it in the sidebar in `_quarto.yml` |
| Add a blog post | copy a folder in `blog/posts/`, rename it, edit |
| Add a paper | `articles/articles.yml` |

## Embedding a video

Each lesson has a commented-out video line near the top. Paste your YouTube link into it, then remove the `<!--`, `-->`, `/*` and `*/` around it.
