#!/usr/bin/env python3
"""Find missing covers; write reviewable candidates without changing book data.
Run: python3 scripts/improve-covers.py --output /tmp/cover-candidates.json
Review images and merge approved cover fields into data/books.json, then export.
"""
import argparse, concurrent.futures, difflib, json, re, unicodedata, urllib.parse, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def norm(s):
    return re.sub(r'[^a-z0-9 ]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PersonalReadingList/1.0'}),timeout=10) as r:return r.read()
def lookup(b):
    try:
        title=b['title'].split(':')[0]
        author=norm(b['author'].split('&')[0]).split()[-1]
        q=urllib.parse.urlencode({'title':title,'author':author,'limit':5,'fields':'key,title,author_name,cover_i,isbn'})
        docs=json.loads(get('https://openlibrary.org/search.json?'+q)).get('docs',[])
        for d in docs:
            if not d.get('cover_i'):continue
            if difflib.SequenceMatcher(None,norm(title),norm(d['title'].split(':')[0])).ratio()<.8:continue
            if not any(author in norm(a).split() for a in d.get('author_name',[])):continue
            url=f"https://covers.openlibrary.org/b/id/{d['cover_i']}-M.jpg?default=false"
            data=get(url)
            if not data.startswith(b'\xff\xd8') or len(data)<2000:continue
            path=f"assets/covers/{b['id']}.jpg";(ROOT/path).write_bytes(data)
            return b['id'],{'cover':path,'coverSource':url,'coverWork':'https://openlibrary.org'+d['key']}
    except Exception as e:print(b['title'],type(e).__name__,flush=True)
    return b['id'],None
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',default='/tmp/cover-candidates.json');p.add_argument('--workers',type=int,default=3);a=p.parse_args()
    books=[b for b in json.loads((ROOT/'data/books.json').read_text()) if not b.get('cover')]
    result={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        for key,data in pool.map(lookup,books):
            if data:result[key]=data
            Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(f'Found {len(result)} candidates for {len(books)} missing covers.')
