#!/usr/bin/env python3
"""Regenerate browser data and update the displayed month after a site update."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
def export_browser_data():
    books=json.loads((ROOT/'data/books.json').read_text())
    assert isinstance(books,list) and all(b.get('title') and b.get('author') for b in books)
    path=ROOT/'data/source.json'
    meta=json.loads(path.read_text()) if path.exists() else {}
    updated=datetime.now(ZoneInfo('America/New_York'))
    meta['updatedOn']=updated.date().isoformat()
    meta['updatedMonth']=updated.strftime('%B %Y')
    path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    browser_meta={'updatedMonth':meta['updatedMonth']}
    (ROOT/'data/books.js').write_text('window.BOOKS = '+json.dumps(books,ensure_ascii=False).replace('<','\\u003c')+';\nwindow.LIBRARY_META = '+json.dumps(browser_meta)+';\n')
    print(f'Exported {len(books)} books; updated {meta["updatedMonth"]}.')
if __name__=='__main__': export_browser_data()
