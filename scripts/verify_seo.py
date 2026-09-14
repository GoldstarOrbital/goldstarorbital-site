"""Verify canonical inventory, metadata, structured data, and local link targets."""
import json
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
from seo_common import ROOT, ORIGIN, PAGES

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.tags=[]; self.ids=set(); self.schemas=[]; self.schema=False; self.buffer=''; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if 'id' in a: self.ids.add(a['id'])
        if tag=='script' and a.get('type')=='application/ld+json': self.schema=True; self.buffer=''
    def handle_data(self,text):
        if self.schema: self.buffer+=text
    def handle_endtag(self,tag):
        if tag=='script' and self.schema: self.schemas.append(json.loads(self.buffer)); self.schema=False

pages={r:Page((ROOT/('index.html' if r=='/' else r[1:]+'.html')).read_text(encoding='utf-8')) for r in PAGES}
titles=set()
for route,p in pages.items():
    info=PAGES[route]
    assert info['title'] not in titles; titles.add(info['title'])
    assert sum(t=='h1' for t,a in p.tags)==1,route
    assert sum(t=='title' for t,a in p.tags)==1,route
    assert [a['href'] for t,a in p.tags if t=='link' and a.get('rel')=='canonical']==[ORIGIN+route],route
    assert len(p.schemas)==1,route
    assert len([a for t,a in p.tags if t=='meta' and a.get('name')=='description'])==1,route
    for node in p.schemas[0]['@graph']:
        if node['@type']=='FAQPage':
            assert len(node['mainEntity'])==len(info['faq'])
            text=(ROOT/(route[1:]+'.html')).read_text(encoding='utf-8')
            from html import escape
            for q,a in info['faq']: assert escape(q) in text and escape(a) in text
    for tag,attrs in p.tags:
        for key in ['href','src']:
            value=attrs.get(key,''); url=urlsplit(value)
            if not value or url.scheme or url.netloc: continue
            target=unquote(url.path) or route
            if target.startswith('/') and target in pages:
                if url.fragment: assert unquote(url.fragment) in pages[target].ids,(route,value)
            else:
                file=ROOT/target.lstrip('/')
                assert file.is_file(),(route,value)
            if tag=='img': assert 'alt' in attrs,(route,value)
locs=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('.//{*}loc')]
assert set(locs)=={ORIGIN+r for r in PAGES}
assert 'Sitemap: '+ORIGIN+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
assert 'noindex' in (ROOT/'404.html').read_text()
print(f'PASS: {len(pages)} pages; canonical URLs, unique titles, descriptions, H1s, JSON-LD/FAQ parity, internal links/fragments, image alt text, sitemap and robots.')
