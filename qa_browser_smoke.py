import os,json,re,subprocess,threading,time,statistics
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
root=Path('/mnt/data/blackout_qa/blackout_game')
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw): super().__init__(*a,directory=str(root),**kw)
 def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',8767),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
def add(test,status,details=''): results.append(dict(test=test,status=status,details=details))
html=(root/'index.html').read_text()
for asset in ['blue.glb','mantaray-XHD.glb','blackoutprotocol.jpg','blackoutprotocol.mp3']:
 add('asset '+asset,'PASS' if (root/asset).exists() else 'FAIL',str((root/asset).stat().st_size if (root/asset).exists() else 0)+' bytes')
for i in range(1,6):
 pat=rf"num:\s*['\"]?0?{i}['\"]?"
 add('mission '+str(i)+' definition','PASS' if re.search(pat,html) else 'NOT VERIFIED','Static source search only')
with sync_playwright() as p:
 for name,opts in [('desktop',dict(viewport={'width':1440,'height':900})),('mobile',dict(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)),('tablet',dict(viewport={'width':820,'height':1180},is_mobile=True,has_touch=True))]:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--disable-web-security'])
  ctx=browser.new_context(**opts)
  page=ctx.new_page(); errors=[];console=[]; failed=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.on('console',lambda msg:console.append(msg.text) if msg.type=='error' else None)
  page.on('requestfailed',lambda req:failed.append(req.url))
  page.set_content(html,wait_until='domcontentloaded');page.wait_for_timeout(400)
  gl=page.evaluate('''() => {const c=document.createElement('canvas');let gl=c.getContext('webgl2')||c.getContext('webgl');return {available:!!gl,version:gl?gl.getParameter(gl.VERSION):null,renderer:gl?gl.getParameter(gl.RENDERER):null}}''')
  add(name+' WebGL context','PASS' if gl['available'] else 'BLOCKED',str(gl))
  add(name+' startup scene','PASS' if not errors and not console else 'BLOCKED', '; '.join((errors+console)[:3])[:500])
  add(name+' external request','PASS' if not failed else 'BLOCKED', str(failed[:5]))
  add(name+' input elements', 'PASS' if page.locator('#btnStart').count() and page.locator('#btnQuality').count() and page.locator('#btnDeploy').count() else 'FAIL','Buttons available in DOM, gameplay callback not exercised')
  add(name+' viewport CSS','PASS' if page.evaluate('document.documentElement.scrollWidth <= innerWidth+2') else 'FAIL',f"scrollWidth={page.evaluate('document.documentElement.scrollWidth')}")
  page.screenshot(path=f'/mnt/data/blackout_qa/{name}_boot.png')
  browser.close()
server.shutdown()
(root/'qa_report.json').write_text(json.dumps(results,indent=2))
for r in results: print(r['status'],r['test'],r['details'][:130])
