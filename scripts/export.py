#!/usr/bin/env python3
"""Regenerate browser data and update the displayed month after a site update."""
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]

def author_names(author):
    """Split source credits while keeping suffixes such as 'Jr.' with a name."""
    names=[]
    for part in re.split(r'\s*(?:,|;|&|\band\b)\s*',author,flags=re.I):
        part=part.strip()
        if not part:
            continue
        if names and re.fullmatch(r'(?:Jr\.?|Sr\.?|II|III|IV)',part,re.I):
            names[-1]+=', '+part
        else:
            names.append(part)
    return names

def export_browser_data():
    books=json.loads((ROOT/'data/books.json').read_text())
    assert isinstance(books,list) and all(b.get('title') and b.get('author') for b in books)
    browser_books=[]
    for book in books:
        # An explicit list handles ambiguous credits without changing source text.
        authors=book.get('authors',author_names(book['author']))
        assert isinstance(authors,list) and authors and all(isinstance(a,str) and a.strip() for a in authors)
        browser_books.append({**book,'authors':authors})
    path=ROOT/'data/source.json'
    meta=json.loads(path.read_text()) if path.exists() else {}
    updated=datetime.now(ZoneInfo('America/New_York'))
    meta['updatedOn']=updated.date().isoformat()
    meta['updatedMonth']=updated.strftime('%B %Y')
    path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    browser_meta={'updatedMonth':meta['updatedMonth']}
    (ROOT/'data/books.js').write_text('window.BOOKS = '+json.dumps(browser_books,ensure_ascii=False).replace('<','\\u003c')+';\nwindow.LIBRARY_META = '+json.dumps(browser_meta)+';\n')
    print(f'Exported {len(books)} books; updated {meta["updatedMonth"]}.')
if __name__=='__main__': export_browser_data()
