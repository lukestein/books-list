# The Reading Room

A quiet, cover-first gallery of books read. One search box filters title and author instantly, including accent-insensitive and mixed title/author searches. Responsive, keyboard accessible, and entirely static. No dependencies, build, API keys, tracking, or runtime network requests are needed. Covers are downloaded into the repository.

## View

Open `index.html` directly, or serve this directory with `python3 -m http.server 8000` and visit http://localhost:8000.

## GitHub Pages

1. Put this directory's contents at the root of your GitHub repo and push to `main`.
2. In the repo's **Settings → Pages → Build and deployment**, select **GitHub Actions**.
3. The included workflow deploys on pushes to `main` and can be run manually in Actions. If your default branch differs, edit `.github/workflows/pages.yml`.

All asset paths are relative, so both `username.github.io` and `username.github.io/repo-name/` work. Publishing the repo and enabling Pages have not been done by this local project.

## Refresh from the reading list

Requires Python 3.10+ and internet access, with no packages to install:

```sh
python3 scripts/refresh.py 'https://p.fsnot.es/xq3vxou4cf/' --covers
```

Use a new FSNotes URL or a saved HTML file in place of that URL. The importer expects a table with columns number, title, author, and optional summary. It preserves source order and all rows, including repeated readings. Stable IDs use title and author. Existing cover choices are retained, and only new/missing covers are requested. A failed page fetch or unrecognized table leaves existing data untouched. Missing images get a decorative text jacket; these are placeholders, not actual covers.

The script writes `data/books.json` (editable canonical records) and `data/books.js` (the same data as a browser script so the page also works from disk). After manual JSON edits, run:

```sh
python3 scripts/export.py
```

Commit changed data and covers, then push. To update via an agent, ask it:

> Refresh the reading room from UPDATED_URL using scripts/refresh.py with --covers. Preserve the existing design and cover overrides. Review unmatched covers and changes in book count, then commit the data and images.

There is no automatic refresh on page load; changes are reviewed and checked into Git.

## Covers and corrections

The importer searches Open Library by title and author and downloads medium JPEG covers. It records the original image URL and matched work link with each successful result. Covers may represent a different edition from the one read, and automatic matches can need review. To correct one, place a JPEG in `assets/covers/`, change that book's `cover` path and provenance fields in `data/books.json`, then export. Local cover overrides survive refreshes. To retry a match, remove its cover fields before refreshing.

Book cover artwork remains the property of its respective rights holders; downloading an image does not transfer rights. Metadata source: [the original FSNotes list](https://p.fsnot.es/xq3vxou4cf/). Image source: [Open Library](https://openlibrary.org/) and its [Covers API](https://openlibrary.org/dev/docs/api/covers).

## Files

- `index.html`, `style.css`, `app.js`: page, styling, filter behavior.
- `data/books.json`, `data/books.js`: book records and browser data.
- `assets/covers/`: local cover images.
- `scripts/refresh.py`: repeatable import and cover downloads.
- `scripts/export.py`: regenerate browser data after manual edits.
- `.github/workflows/pages.yml`: GitHub Pages deployment.

Design copy, colors, and title can be changed directly in HTML and CSS.
