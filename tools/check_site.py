#!/usr/bin/env python3
"""Validate local pages, asset paths, anchors, content boundaries and metadata."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'
DEMO_ENTRY='https://demo.mywavelink.com/__demo/public'
HOME_DEMO_LINKS={DEMO_ENTRY} | {f'{DEMO_ENTRY}?area={area}' for area in ('inventory', 'hr', 'it')}
DEMO_LINK_COUNTS={'privacy.html':2,'404.html':1}
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
 errors=[];checks=[];pages={p.name:Page(p.read_text(encoding='utf-8')) for p in SITE.glob('*.html')}
 for name,page in pages.items():
  if len(set(page.ids))!=len(page.ids):errors.append(name+': duplicate IDs')
  if page.h1!=1:errors.append(name+': expected one h1')
  demo_links=[a for a in page.links if urlsplit(a.get('href','')).hostname=='demo.mywavelink.com']
  if name in DEMO_LINK_COUNTS and len(demo_links)!=DEMO_LINK_COUNTS[name]:errors.append(name+': missing public demo link')
  destinations={a.get('href') for a in demo_links}
  if name=='index.html' and destinations!=HOME_DEMO_LINKS:errors.append(name+': expected general, inventory, HR and IT demo entry points')
  if name!='index.html' and destinations-{DEMO_ENTRY}:errors.append(name+': unexpected public demo destination')
  for a in page.links:
   u=urlsplit(a.get('href',''))
   if u.scheme or u.netloc:
    if u.scheme not in ('https','mailto'):errors.append(name+': unexpected external scheme')
    if a.get('target')=='_blank' and not {'noopener','noreferrer'}<=set(a.get('rel','').split()):errors.append(name+': new-tab link missing protection')
    continue
   target=u.path.lstrip('/') or name
   if target=='/':target='index.html'
   if a.get('href')=='/':target='index.html'
   if target not in pages:
    if u.fragment or not (SITE/target).is_file():errors.append(name+': missing local link target '+target)
   elif u.fragment and unquote(u.fragment) not in pages[target].ids:errors.append(name+': missing anchor '+a['href'])
  for source in page.assets:
   u=urlsplit(source)
   if u.scheme or u.netloc:continue
   if not (SITE/u.path.lstrip('/')).is_file():errors.append(name+': missing asset '+source)
  checks.append({'page':name,'h1':page.h1,'links':len(page.links),'anchors':len(page.ids)})
 home=(SITE/'index.html').read_text(encoding='utf-8');css=(SITE/'styles.css').read_text(encoding='utf-8');js=(SITE/'script.js').read_text(encoding='utf-8')
 expected=['Inventory &amp; boxes','Manifests &amp; receiving']
 # Generated text uses literal ampersands; test human text and the stored HTML equivalently.
 for term in ['Inventory & boxes','Manifests & receiving','Fault reports','HSE / QSHE','QR document signing','Daily & hitch handovers','Optional email alerts','Two-step verification','Original Files','Worksheet imports']:
  if term not in home:errors.append('Missing capability: '+term)
 ai_section=re.search(r'<section[^>]*id="ai-assistance"[^>]*>(.*?)</section>',home,re.S)
 hero=re.search(r'<section[^>]*class="hero"[^>]*>(.*?)</section>',home,re.S)
 hero_links=Page(hero[1]).links if hero else []
 if not any(a.get('href')==DEMO_ENTRY for a in hero_links):errors.append('Missing live demo action in the hero')
 if not any(urlsplit(a.get('href','')).scheme=='mailto' and urlsplit(a['href']).path=='comercial@mywavelink.com' for a in hero_links):
  errors.append('Missing commercial walkthrough action in the hero')
 if not (HOME_DEMO_LINKS-{DEMO_ENTRY}) <= {a.get('href') for a in hero_links}:errors.append('Missing direct guest routes in the hero')
 for term in ['S/N → Serial number','Qty → Quantity','Confirm and import']:
  if term not in home:errors.append('Missing worksheet example: '+term)
 platform=re.search(r'<section\b[^>]*\bid="platform"',home)
 if not hero or not platform or platform.start()<hero.end() or re.search(r'<section\b',home[hero.end():platform.start()]):
  errors.append('The platform must be the first section after the hero')
 if 'class="journey-section workflow-story section"' in home or 'Follow a sensor rack from shore to handover' in home:
  errors.append('The illustrative workflow must not be present')
 if '<span id="workflow" class="legacy-section-anchor" aria-hidden="true"></span>' not in home:
  errors.append('Missing legacy workflow bookmark')
 navigation=re.search(r'<nav\b[^>]*\bid="main-navigation"[^>]*>(.*?)</nav>',home,re.S)
 if not ai_section or not navigation or not any(a.get('href')=='#ai-assistance' for a in Page(navigation[1]).links):
  errors.append('Missing AI section or navigation link')
 else:
  area=ai_section[1]
  if area.count('<details name="ai-examples"')!=3:errors.append('Expected three non-import AI examples')
  for term in ['If enabled by your company, the OpenAI API','You decide what to keep','href="privacy.html#openai"',f'href="{DEMO_ENTRY}"']:
   if term not in area:errors.append('Missing AI section content: '+term)
 if home.count('class="platform-choice"')!=7:errors.append('Expected seven explorer categories')
 if home.count('class="capability"')!=20:errors.append('Expected 20 capability areas including HR and IT')
 if home.count('id="package-')!=4:errors.append('Expected four HR areas')
 for term in ['Crew & Planning','Timesheets & Approvals','Travel & Expenses','Personal Documents','Fictional crew records','Confirm the installed application version, HR permissions and deployment scope with the team.','href="#packages"']:
  if term not in home:errors.append('Missing HR content/destination: '+term)
 for term in ['comercial@mywavelink.com','support@mywavelink.com',DEMO_ENTRY,'https://www.mywavelink.com/']:
  if term not in home:errors.append('Missing destination: '+term)
 for term in ['localStorage','sessionStorage','document.cookie','XMLHttpRequest','fetch(']:
  if term in js:errors.append('Unexpected website data operation: '+term)
 for name in ('index.html','privacy.html','404.html'):
  if '?v=3.3.5' not in (SITE/name).read_text(encoding='utf-8'):errors.append(name+': stale cache version')
 if '<source media="(max-width: 740px)" srcset="assets/offshore-operations-small.webp">' not in home:errors.append('Missing responsive hero image')
 if 'prefers-reduced-motion' not in css:errors.append('Missing reduced motion handling')
 if re.search(r'(?:email sign-in|two-step verification).{0,60}planned',home,re.I):errors.append('Stale planned security label')
 # All structured data must parse as exact JSON.
 for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',home,re.S):json.loads(raw)
 result={'version':'3.3.5','passed':not errors,'checks':checks,'errors':errors}
 print(json.dumps(result,indent=2));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
