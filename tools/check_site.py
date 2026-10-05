#!/usr/bin/env python3
"""Validate local pages, asset paths, anchors, content boundaries and metadata."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.assets=[];self.h1=0;self.text=[];self.scripts=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='a':self.links.append(a)
  if tag in ('img','script','source','link'):
   for key in ('src','srcset','href'):
    if key in a:self.assets.append(a[key])
  if tag=='script':self.scripts.append(a)
 def handle_data(self,d):self.text.append(d)
def main():
 errors=[];checks=[];pages={p.name:Page(p.read_text()) for p in SITE.glob('*.html')}
 for name,page in pages.items():
  if len(set(page.ids))!=len(page.ids):errors.append(name+': duplicate IDs')
  if page.h1!=1:errors.append(name+': expected one h1')
  for a in page.links:
   u=urlsplit(a.get('href',''))
   if u.scheme or u.netloc:
    if u.scheme not in ('https','mailto'):errors.append(name+': unexpected external scheme')
    if a.get('target')=='_blank' and not {'noopener','noreferrer'}<=set(a.get('rel','').split()):errors.append(name+': new-tab link missing protection')
    continue
   target=u.path.lstrip('/') or name
   if target=='/':target='index.html'
   if a.get('href')=='/':target='index.html'
   if target not in pages:errors.append(name+': missing page '+target)
   elif u.fragment and unquote(u.fragment) not in pages[target].ids:errors.append(name+': missing anchor '+a['href'])
  for source in page.assets:
   u=urlsplit(source)
   if u.scheme or u.netloc:continue
   if not (SITE/u.path.lstrip('/')).is_file():errors.append(name+': missing asset '+source)
  checks.append({'page':name,'h1':page.h1,'links':len(page.links),'anchors':len(page.ids)})
 home=(SITE/'index.html').read_text();css=(SITE/'styles.css').read_text();js=(SITE/'script.js').read_text()
 expected=['Inventory &amp; boxes','Manifests &amp; receiving']
 # Generated text uses literal ampersands; test human text and the stored HTML equivalently.
 for term in ['Inventory & boxes','Manifests & receiving','Fault reports','HSE / QSHE','QR document signing','Daily & hitch handovers','Optional email alerts','Two-step verification','Original Files','Excel worksheet recognition']:
  if term not in home:errors.append('Missing capability: '+term)
 if home.count('class="platform-choice"')!=7:errors.append('Expected seven explorer categories')
 if home.count('class="capability"')!=18:errors.append('Expected 18 capability areas')
 if home.count('class="package-status">Planned package')!=4:errors.append('Expected four clearly planned HR packages')
 for term in ['Crew & Rotations','Timesheets & Approvals','Travel & Expenses','People & Readiness','ILLUSTRATIVE CONCEPT · FICTIONAL DATA','Scope, release dates and commercial terms are to be confirmed.','href="#packages"']:
  if term not in home:errors.append('Missing planned package boundary/destination: '+term)
 for term in ['comercial@mywavelink.com','support@mywavelink.com','https://demo.mywavelink.com/','https://www.mywavelink.com/']:
  if term not in home:errors.append('Missing destination: '+term)
 for term in ['localStorage','sessionStorage','document.cookie','XMLHttpRequest','fetch(']:
  if term in js:errors.append('Unexpected website data operation: '+term)
 for name in ('index.html','privacy.html','404.html'):
  if '?v=3.1.0' not in (SITE/name).read_text():errors.append(name+': stale cache version')
 if 'prefers-reduced-motion' not in css:errors.append('Missing reduced motion handling')
 if re.search(r'(?:email sign-in|two-step verification).{0,60}planned',home,re.I):errors.append('Stale planned security label')
 # All structured data must parse as exact JSON.
 for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',home,re.S):json.loads(raw)
 result={'version':'3.1.0','passed':not errors,'checks':checks,'errors':errors}
 print(json.dumps(result,indent=2));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
