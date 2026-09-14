"""Build static guide/product pages, shared metadata, sitemap, and architecture."""
from pathlib import Path
from html import escape
import re
import runpy
import xml.etree.ElementTree as ET
from seo_common import ROOT, ORIGIN, PAGES, decorate, header, footer

def links(paths):
    return '<div class="related-grid">'+''.join(f'<a href="{path}"><strong>{escape(PAGES[path]["label"])}</strong><span>{escape(PAGES[path]["description"])}</span><span aria-hidden="true">↗</span></a>' for path in paths)+'</div>'

def faq(info):
    if not info.get('faq'): return ''
    return '<section id="questions"><h2>Questions answered</h2>'+''.join(f'<article class="direct-answer"><h3>{escape(q)}</h3><p>{escape(a)}</p></article>' for q,a in info['faq'])+'</section>'

def make_page(route,info):
    content=(ROOT/'content'/f'{route[1:]}.html').read_text(encoding='utf-8')
    toc=''.join(f'<li><a href="#{id}">{text}</a></li>' for id,text in re.findall(r'<section id="([^"]+)"><h2>(.*?)</h2>',content))
    if info.get('faq'): toc+='<li><a href="#questions">Questions answered</a></li>'
    breadcrumbs='<a href="/">Home</a><span aria-hidden="true"> / </span>'
    if info['type']=='TechArticle': breadcrumbs+='<a href="/guides">Research guides</a><span aria-hidden="true"> / </span>'
    breadcrumbs+=f'<span aria-current="page">{escape(info["label"])}</span>'
    byline=f'<p class="byline">Published by <a href="/about">Goldstar Orbital, Inc.</a> · Updated <time datetime="{info["updated"]}">September 14, 2026</time></p>'
    actions=''
    match=re.search(r'<div class="page-actions">.*?</div>',content,re.S)
    if match:
        actions=match.group()
        content=content.replace(actions,'',1)
    image=''
    if route not in ['/guides','/about']:
        alt={'/functioning-faith':'Functioning Faith community and activity home screen','/fawn':'Fawn product sign-in screen'}.get(route,info['label']+' concept schematic; proposed design, not flight-qualified hardware')
        w,h={'/fawn':(440,716),'/functioning-faith':(1208,716)}.get(route,(1200,760))
        image=f'<figure class="guide-figure"><a href="{info["image"]}" target="_blank" rel="noopener"><img src="{info["image"]}" width="{w}" height="{h}" alt="{escape(alt)}" loading="lazy" decoding="async"></a><figcaption>{escape(alt)}. Open the image at full size.</figcaption></figure>'
    body=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080a0b"><link rel="icon" href="/assets/favicon-32.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=Space+Mono&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="/site.css"></head><body class="guide-page"><a class="skip" href="#main">Skip to content</a>{header(route)}<main id="main"><article class="guide-wrap"><nav class="breadcrumbs" aria-label="Breadcrumb">{breadcrumbs}</nav><p class="eyebrow">{ 'RESEARCH GUIDE' if info['type']=='TechArticle' else 'GOLDSTAR ORBITAL' }</p><h1>{escape(info['heading'])}</h1>{byline}<div class="answer-lead"><p>{escape(info['answer'])}</p></div><nav class="contents" aria-label="On this page"><h2>On this page</h2><ul>{toc}</ul></nav>{image}<div class="guide-body">{content}{faq(info)}</div><aside class="related" aria-label="Related pages"><h2>Continue exploring</h2>{links(info['related'])}</aside></article></main>{footer()}</body></html>'''
    body=body.replace('<nav class="contents"',actions+'<nav class="contents"',1)
    (ROOT/f'{route[1:]}.html').write_text(decorate(body,route),encoding='utf-8')

def build():
    home=(ROOT/'index.html').read_text(encoding='utf-8')
    home=home.replace('From the way we connect on Earth<br>to the infrastructure beyond it.<br>We build with the next horizon in mind.','Goldstar Orbital explores photonic space infrastructure<br>and builds digital ventures for everyday life.<br>Discover Fawn and Functioning Faith.')
    home=home.replace('Three worlds.<br>One driving curiosity.','Our ventures.<br>One driving curiosity.')
    def video_preview(m):
        video,title=m.group(1),m.group(2)
        preview='fawn-preview.jpg' if video=='ijnjv6NTWS8' else 'faith-preview.jpg'
        return f'<a class="film-preview" href="https://www.youtube.com/watch?v={video}" data-video="{video}" aria-label="Play {title}"><img src="/assets/{preview}" alt="" loading="lazy" decoding="async"><span>▶ Play {title}</span></a>'
    home=re.sub(r'<iframe src="https://www.youtube-nocookie.com/embed/([^"]+)" title="([^"]+)"[^>]*></iframe>',video_preview,home)
    if 'src="/videos.js"' not in home: home=home.replace('</head>','<script src="/videos.js" defer></script></head>',1)
    home=home.replace('href="https://goldstarorbital.github.io/fawn-landing/index.html" target="_blank" rel="noopener">Discover Fawn','href="/fawn">Discover Fawn')
    home=home.replace('href="https://faithfit-demo-production.up.railway.app" target="_blank" rel="noopener">Explore Functioning Faith','href="/functioning-faith">Explore Functioning Faith')
    block='<section class="section home-guides" id="research-guides"><p class="eyebrow">THE RESEARCH, EXPLAINED</p><h2>Photonic computing.<br>Real engineering questions.</h2><p class="section-intro">Explore the thinking behind our spacecraft concept, from matrix operations to heat rejection and satellite-assisted photosynthesis.</p>'+links(['/photonic-computing','/orbital-infrastructure','/mars-photosynthesis'])+'<a class="text-link" href="/guides">Browse all research guides ↗</a></section>'
    if '<!-- GUIDES:START -->' in home: home=re.sub(r'<!-- GUIDES:START -->.*?<!-- GUIDES:END -->',lambda m:'<!-- GUIDES:START -->'+block+'<!-- GUIDES:END -->',home,flags=re.S)
    else: home=home.replace('<section class="section contact"','<!-- GUIDES:START -->'+block+'<!-- GUIDES:END -->\n<section class="section contact"',1)
    home=home.replace('src="assets/fawn-logo.png"','src="assets/fawn-logo-small.webp"').replace('src="/assets/fawn-logo.png"','src="/assets/fawn-logo-small.webp"')
    for src,w,h in [('fawn-preview.jpg',440,716),('faith-preview.jpg',1208,716),('schematics/rev-b/satellite.svg',1200,760)]:
        home=re.sub(r'(<img\b[^>]*src="/?assets/'+re.escape(src)+r'"[^>]*)(>)',lambda m:m[1]+(' width="'+str(w)+'" height="'+str(h)+'" decoding="async"' if 'width=' not in m[1] else '')+m[2],home)
    (ROOT/'index.html').write_text(decorate(home,'/'),encoding='utf-8')
    runpy.run_path(str(ROOT/'scripts/build_architecture.py'),run_name='__main__')
    for route,info in PAGES.items():
        if route not in ['/','/architecture']: make_page(route,info)
    namespace='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',namespace)
    sitemap=ET.Element('{'+namespace+'}urlset')
    for route,info in PAGES.items():
        url=ET.SubElement(sitemap,'{'+namespace+'}url')
        ET.SubElement(url,'{'+namespace+'}loc').text=ORIGIN+route
        ET.SubElement(url,'{'+namespace+'}lastmod').text=info['updated']
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    print(f'Built {len(PAGES)} canonical pages and sitemap.xml')

if __name__=='__main__': build()
