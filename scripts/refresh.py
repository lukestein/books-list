#!/usr/bin/env python3
"""Import an FSNotes table, preserving cover choices by title + author."""
import argparse, concurrent.futures, hashlib, html, json, re, time, urllib.request, urllib.parse
from pathlib import Path
from datetime import datetime, timezone
from export import export_browser_data
ROOT = Path(__file__).resolve().parents[1]
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent':'PersonalBookshelf/1.0 (static reading archive)'})
    with urllib.request.urlopen(req, timeout=20) as response: return response.read()
def parse(source):
    books=[]
    for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>', source, re.S|re.I):
        cells=[html.unescape(re.sub('<[^>]+>', '', c)).strip() for c in re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.S|re.I)]
        if len(cells)<3 or not cells[1] or not cells[2]: continue
        title,author=cells[1:3]
        key=hashlib.sha256((title+'\0'+author).encode()).hexdigest()[:16]
        book=dict(id=key,title=re.sub(r'\s*\[re-read\]', '', title, flags=re.I).strip(),author=author,summary=cells[3] if len(cells)>3 else '')
        if book['title'] != title: book.update(sourceTitle=title,reread=True)
        books.append(book)
    if not books: raise ValueError('No book table found; existing data was not changed.')
    return books

def cover(book):
    if book.get('cover') and (ROOT/book['cover']).exists(): return book
    try:
        query=urllib.parse.urlencode({'title':book['title'],'author':re.sub(r'[.]+', ' ', book['author']),'limit':3,'fields':'key,title,author_name,cover_i'})
        docs=json.loads(get('https://openlibrary.org/search.json?'+query)).get('docs',[])
        doc=next((d for d in docs if d.get('cover_i')),None)
        if doc:
            url=f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg?default=false"
            data=get(url)
            if not data.startswith(b'\xff\xd8') or len(data)<1500: raise ValueError('Missing cover')
            path=f"assets/covers/{book['id']}.jpg"
            (ROOT/path).write_bytes(data)
            book.update(cover=path,coverSource=url,coverWork='https://openlibrary.org'+doc['key'])
    except Exception as e:
        print(f"No cover: {book['title']} ({type(e).__name__})",flush=True)
    return book

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',nargs='?',default='https://p.fsnot.es/xq3vxou4cf/')
    p.add_argument('--covers',action='store_true');p.add_argument('--workers',type=int,default=2)
    args=p.parse_args()
    raw=get(args.source).decode() if args.source.startswith(('http://','https://')) else Path(args.source).read_text()
    books=parse(raw)
    dest=ROOT/'data/books.json'
    old={b['id']:b for b in json.loads(dest.read_text())} if dest.exists() else {}
    for b in books:
        for k in ('cover','coverSource','coverWork'):
            if k in old.get(b['id'],{}): b[k]=old[b['id']][k]
    def save():
        dest.write_text(json.dumps(books,ensure_ascii=False,indent=2)+'\n')
        # Also works when opened directly from disk, with no fetch or server required.
        (ROOT/'data/books.js').write_text('window.BOOKS = '+json.dumps(books,ensure_ascii=False).replace('<','\\u003c')+';\n')
    save()
    (ROOT/'data/source.json').write_text(json.dumps({
        'source': args.source,
        'importedOn': datetime.now(timezone.utc).date().isoformat(),
        'recordCount': len(books),
        'order': 'Original source order; not assumed to be chronological',
        'coverProvider': 'Open Library'
    }, indent=2)+'\n')
    if args.covers:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            for i,b in enumerate(pool.map(cover,books)):
                books[i]=b
                if i%10==0: save();print(f'Processed {i+1}/{len(books)}',flush=True)
        save()
    export_browser_data()
    print(f"Saved {len(books)} books; {sum(bool(b.get('cover')) for b in books)} local covers.")
if __name__=='__main__': main()
