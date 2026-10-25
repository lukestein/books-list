# Maintaining this reading gallery

Keep this a buildless static website suitable for GitHub Pages. Do not add a server or runtime API dependency for list updates.

For an updated FSNotes URL, run `python3 scripts/refresh.py 'URL' --covers`. Keep source order, repeated readings, and all title/author data. Inspect the change in record count before accepting a refresh. Summaries are retained as source data but are intentionally absent from the simple gallery and search.

`data/books.json` is the editable source; run `python3 scripts/export.py` after manual changes so `data/books.js` stays synchronized. The refresh script writes both files. Preserve local cover overrides and attribution. Do not treat a missing cover as a reason to drop a book.

Verify search by author, title, accented text, a query with no matches, and clearing the field. Check narrow screens for overflow. Keep one search input; additional controls need a user request.

Publication target is the user's GitHub repository. The included GitHub Actions workflow deploys the root static assets. Do not publish to a separate hosting service unless requested.

Keep the compact header, blank search box (with accessible label), subtle source-position numbers, and re-read asterisk convention. Run `scripts/export.py` to refresh browser metadata. The workflow also exports on deployment, using America/New_York for the displayed month. Do not put a link to the private source list in the public UI.

Display the gallery in reverse input order (newest first), while retaining source-position book numbers. Keep stored data in source order. The HTML document title is “Luke’s book list”.
