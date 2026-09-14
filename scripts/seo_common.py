"""Shared static metadata and navigation. No JavaScript is required for SEO content."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://goldstarorbital.com'
PAGES = json.loads((ROOT / 'content/pages.json').read_text(encoding='utf-8'))
ORG = ORIGIN + '/#organization'
SITE = ORIGIN + '/#website'

def header(route='/'):
    links = [('/#products', 'Ventures', 'ventures'), ('/architecture', 'Architecture', 'architecture'), ('/guides', 'Guides', 'guides'), ('/about', 'About', 'about')]
    nav = ''.join(f'<a href="{url}" data-nav="{key}"'+(' aria-current="page"' if route == url else '')+f'>{label}</a>' for url,label,key in links)
    return '<header class="header"><a class="brand" href="/" aria-label="Goldstar Orbital home"><span class="brand-star" aria-hidden="true">✦</span><span>GOLDSTAR<span class="brand-sub">O R B I T A L</span></span></a><nav aria-label="Main navigation">'+nav+'</nav><a class="contact-link" href="/about#contact">Let’s talk <span aria-hidden="true">↗</span></a></header>'

def footer():
    return '''<footer><a class="brand" href="/" aria-label="Goldstar Orbital home"><span class="brand-star" aria-hidden="true">✦</span><span>GOLDSTAR<span class="brand-sub">O R B I T A L</span></span></a><span>© 2026 Goldstar Orbital, Inc.</span><nav aria-label="Footer navigation"><a href="/guides">Research guides</a><a href="/functioning-faith">Functioning Faith</a><a href="/fawn">Fawn</a><a href="/about">About &amp; contact</a><a href="https://github.com/goldstarorbital" target="_blank" rel="noopener">GitHub ↗</a><a href="https://www.linkedin.com/in/alex-goldsmith-46a911302" target="_blank" rel="noopener">LinkedIn ↗</a><a href="https://x.com/SrGoldy56" target="_blank" rel="noopener">X ↗</a></nav></footer>'''

def graph(route):
    info=PAGES[route]
    url=ORIGIN+route
    org={'@type':'Organization','@id':ORG,'name':'Goldstar Orbital','legalName':'Goldstar Orbital, Inc.','url':ORIGIN+'/','logo':{'@type':'ImageObject','url':ORIGIN+'/assets/favicon-512.png'},'email':'alexgoldsmith@goldstarorbital.com','founder':{'@id':ORIGIN+'/about#founder'},'sameAs':['https://github.com/goldstarorbital']}
    nodes=[org, {'@type':'Person','@id':ORIGIN+'/about#founder','name':'Alexander Marcus Goldsmith','jobTitle':'Founder and CEO','worksFor':{'@id':ORG},'url':ORIGIN+'/about','sameAs':['https://www.linkedin.com/in/alex-goldsmith-46a911302']}, {'@type':'WebSite','@id':SITE,'url':ORIGIN+'/','name':'Goldstar Orbital','publisher':{'@id':ORG},'inLanguage':'en'}]
    page={'@type':info['type'] if info['type'] in ['AboutPage','CollectionPage'] else 'WebPage','@id':url+'#webpage','url':url,'name':info['title'],'description':info['description'],'inLanguage':'en','isPartOf':{'@id':SITE},'publisher':{'@id':ORG},'dateModified':info['updated'],'primaryImageOfPage':{'@type':'ImageObject','url':ORIGIN+info['image']}}
    nodes.append(page)
    if route!='/':
        crumbs=[{'@type':'ListItem','position':1,'name':'Home','item':ORIGIN+'/'}]
        if info['type']=='TechArticle' and route!='/architecture': crumbs.append({'@type':'ListItem','position':2,'name':'Research guides','item':ORIGIN+'/guides'})
        crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':info['label'],'item':url})
        nodes.append({'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':crumbs})
        page['breadcrumb']={'@id':url+'#breadcrumbs'}
    if info['type']=='TechArticle':
        page['mainEntity']={'@id':url+'#article'}
        nodes.append({'@type':'TechArticle','@id':url+'#article','headline':info.get('heading',info['title']),'description':info['description'],'author':{'@id':ORG},'publisher':{'@id':ORG},'datePublished':info['published'],'dateModified':info['updated'],'image':[ORIGIN+info['image']],'mainEntityOfPage':{'@id':url+'#webpage'},'inLanguage':'en','url':url})
    if route=='/guides':
        nodes.append({'@type':'ItemList','@id':url+'#guide-list','itemListElement':[{'@type':'ListItem','position':i+1,'name':PAGES[p]['label'],'url':ORIGIN+p} for i,p in enumerate(info['related'])]})
        page['mainEntity']={'@id':url+'#guide-list'}
    if route=='/functioning-faith':
        nodes.append({'@type':'SoftwareApplication','@id':url+'#app','name':'Functioning Faith','url':url,'description':info['answer'],'applicationCategory':'LifestyleApplication','operatingSystem':'iOS','installUrl':'https://testflight.apple.com/join/SjmBBQbu','publisher':{'@id':ORG}})
        page['mainEntity']={'@id':url+'#app'}
    if info.get('faq'):
        page['hasPart']={'@id':url+'#faq'}
        nodes.append({'@type':'FAQPage','@id':url+'#faq','url':url+'#questions','isPartOf':{'@id':url+'#webpage'},'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in info['faq']]})
    return {'@context':'https://schema.org','@graph':nodes}

def decorate(html,route):
    info=PAGES[route]
    # Clear the generated block first so repeated builds are stable.
    html=re.sub(r'\s*<!-- SEO:START -->.*?<!-- SEO:END -->','',html,flags=re.S)
    head=re.search(r'<head>(.*?)</head>',html,re.S).group(1)
    head=re.sub(r'<title>.*?</title>','',head,flags=re.S)
    head=re.sub(r'<meta\s+[^>]*(?:name|property)=["\'](?:description|robots|og:[^"\']+|twitter:[^"\']+)["\'][^>]*>','',head,flags=re.I)
    head=re.sub(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>','',head,flags=re.I)
    url=ORIGIN+route
    meta='\n<!-- SEO:START -->\n'+f'<title>{escape(info["title"])}</title>\n<meta name="description" content="{escape(info["description"],quote=True)}">\n<meta name="robots" content="index,follow,max-image-preview:large">\n<link rel="canonical" href="{url}">\n'
    for key,value in {'og:title':info['title'],'og:description':info['description'],'og:url':url,'og:site_name':'Goldstar Orbital','og:type':'article' if info['type']=='TechArticle' else 'website','og:locale':'en_US','og:image':ORIGIN+'/assets/orbital-hero.jpg','og:image:alt':'Gold-lit planetary horizon for Goldstar Orbital','twitter:card':'summary_large_image','twitter:title':info['title'],'twitter:description':info['description'],'twitter:image':ORIGIN+'/assets/orbital-hero.jpg','twitter:image:alt':'Gold-lit planetary horizon for Goldstar Orbital'}.items():
        meta+=f'<meta {"property" if key.startswith("og:") else "name"}="{key}" content="{escape(value,quote=True)}">\n'
    meta+='<script type="application/ld+json">'+json.dumps(graph(route),ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>\n<!-- SEO:END -->'
    html=html.replace(re.search(r'<head>.*?</head>',html,re.S).group(),'<head>'+head+meta+'\n</head>',1)
    if 'href="/seo.css"' not in html: html=html.replace('</head>','<link rel="stylesheet" href="/seo.css">\n</head>',1)
    if route in ['/','/architecture'] and 'rel="preload" as="image"' not in html:
        html=html.replace('</head>','<link rel="preload" as="image" href="/assets/orbital-hero.jpg" fetchpriority="high">\n</head>',1)
    html=re.sub(r'<header.*?</header>',lambda m:header(route),html,count=1,flags=re.S)
    html=re.sub(r'<footer>.*?</footer>',lambda m:footer(),html,count=1,flags=re.S)
    html=html.replace('href="index.html#','href="/#').replace('href="architecture.html','href="/architecture')
    html=re.sub(r'<link[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com[^>]*>','',html)
    if 'href="/assets/fonts/fonts.css"' not in html:
        html=html.replace('</head>','<link rel="stylesheet" href="/assets/fonts/fonts.css">\n<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/dm-sans-400.woff2" crossorigin>\n</head>',1)
    html=html.replace('aria-label="Goldstar Orbital home"','aria-label="Goldstar O R B I T A L home"')
    html=html.replace('aria-label="Explore Fawn"','aria-label="Everyday money. A fresh perspective. Explore Fawn"')
    html=html.replace('aria-label="Explore Functioning Faith"','aria-label="Purpose in the everyday. Explore Functioning Faith"')
    # Root-relative assets work on the custom 404 and on canonical clean URLs.
    html=re.sub(r'(href|src)="((?:assets/|site\.css|space\.(?:css|js)|architecture\.(?:css|js))[^\"]*)"',r'\1="/\2"',html)
    return html
