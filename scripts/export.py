#!/usr/bin/env python3
"""Regenerate browser data from manually edited JSON."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
books=json.loads((root/'data/books.json').read_text())
assert isinstance(books,list) and all(b.get('title') and b.get('author') for b in books)
(root/'data/books.js').write_text('window.BOOKS = '+json.dumps(books,ensure_ascii=False).replace('<','\\u003c')+';\n')
print(f'Exported {len(books)} books.')
