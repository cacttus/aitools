# custom img/data extractor
# source bashutils.sh; start_venv
# python3 ./webscraper.py
#
# botd: get the git
# cd ~/git/BotD/
# npm install 
# npm run build
# needs new nodejs version
# download nodejs
# ln -s *dist/bin/node /usr/bin/node
# ln -s *dist/bin/npm /usr/bin/npm
# ln -s *dist/bin/npx /usr/bin/npx


#* splash * phantomjs
import os
import requests
import urllib.request
import time 
import csv
from datetime import datetime
from io import BytesIO
import re
import random
from PIL import Image
from urllib.parse import urlparse
from urllib.request import pathname2url
from fake_useragent import UserAgent
import subprocess
import json
import math

from selenium import webdriver 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from globals import *

class Gu: pass
class Csv: pass
class Config: pass
class Item: pass
class Utils: pass
class LinkStatus:pass

#https://www.selenium.dev/selenium/docs/api/py/api.html
class Config:
  def __init__(self):
    self.data_path = os.path.abspath('./data/')
    self.img_path = os.path.abspath(os.path.join(self.data_path,'img/'))
    self.tmp_path = os.path.abspath(os.path.join(self.data_path,'tmp/'))
    self.html_path = os.path.abspath(os.path.join(self.data_path,'html/'))
    self.links_file = os.path.abspath(os.path.join(self.data_path,'links.csv'))
    self.screenshot_path = os.path.join(self.data_path, f"screenshots/")
    self.ff_root = os.path.join(self.tmp_path,"firefox/")
    self.ff_profile_path = os.path.join(self.ff_root,"profile/")
    self.ff_data_path = os.path.join(self.ff_root,"user-data/")
    self.visit_delay = [2.10223, 0.511652, 1.51136] #delay between http get
    self.scroll_delay = [0.653, 0.2123425, 1.31465] #delay scrol
    self.stay_delay = [40.653, 0.2123425, 120.31465] #et
    self.link_query_delay = [60*60*2, 0, 0] #dleay for querying links
    self.img_min_w = 512
    self.img_min_h = 512
    self.base_url = "https://duckduckgo.com/?q=ass+bear&t=h_&iar=images&iax=images&ia=images"
    #self.base_url = "https://www.scrapethissite.com/pages/advanced/?gotcha=headers"
    #self.base_url = "https://yandex.com/images/search?text=blowjob"
    #self.base_url="https://duckduckgo.com"
    #self.base_url="https://yandex.com/images/search?text=bob%20saget%20face"
    #self.base_url = "https://www.google.com/search?q=blowjob&tbm=isch"
    # ?isize=large
    # ?isize=large medium small
    #_URL="https://yandex.com/images/search?isize=large&text=hot%20cunt%203840x1080%20wet%20pussy"
    # url[string], valid[bool], last_query[datetime], last_success[datetime], query_count[int], success_count[int]  

class Csv:
  def __init__(self, loc):
    self.delim='|'
    self.quot='\''
    self.nl=' '
    self.loc=loc
  def save(self, links):
    with open(self.loc, 'w', newline=self.nl) as f:
      w = csv.writer(f, delimiter=self.delim, quotechar=self.quot, quoting=csv.QUOTE_MINIMAL)
      for link in links:
        w.writerow(dir(link))
  def load(self):
    if os.path.exists(self.loc):
      with open(self.loc, newline=self.nl) as f:
        r = csv.reader(f, delimiter=self.delim, quotechar=self.quot)
        for row in r:
          for col in row:
            pass

class LinkStatus:
  Unset = 0
  Success = 1
  HtmlError = 2
  TooSmall = 3
class LinkType:
  Unset = 0
  Src_Img = 1
  Src_Video = 2
  Href = 3
class SpiderAPI:
  Unset=0
  BeautifulSoup=1 #simple, no js
  Selenium=2 # runs gecko

class Link:
  def __init__(self,url="",valid=False,last_query=datetime.min,last_success=datetime.min,query_count=0,success_count=0,depth=0,status=LinkStatus.Unset):
    self.url:str=url
    self.valid:bool=valid #e.g. not a thumbnail
    self.last_query:datetime=last_query
    self.last_success:datetime=last_success
    self.query_count:int=query_count
    self.success_count:int=success_count
    self.depth=depth #realitve to the root page
    self.status=status
    self._data = None
    self._size = None

def millis():
  return int(round(time.time() * 1000))

def make_fuzzy(tuple):
  return tuple[0] + random.uniform(tuple[1], tuple[2])

def ensure_dir(p):
  if not os.path.exists(p):
    dbg(f"creating '{p}'")
    os.makedirs(p)  

class Utils:
  @staticmethod
  def image_size(url) -> None:
    #first check if size exists
    url.get('width', 'n/a')
    with urllib.request.urlopen(url) as u:
      f = io.BytesIO(u.read())
      img = Image.open(f)
      return img.size # (width, height) tuple
  @staticmethod
  def read_file_string(fn):
    s = ""
    dbg(f"reading {fn}")
    with open(fn, 'r') as f:
      s = f.read()
    return s

class WebScraper: 
      
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    self.driver.close()
    
  def __init__(self):
    msg(f"*** STARTING WEBSCRAPER ***")
    dbg(f"cwd='{os.path.dirname(os.path.realpath(__file__))}'")

    self.api = SpiderAPI.Selenium
    self.config = Config()
    self.img_links = {}
    self.csv = Csv(self.config.links_file)
    self.depth = 0
    self._quit=False
    self._page_height=0
    self._link_tags={} #the hash of he <a> element text => seleneum tag 
    self._next=[] #next urls
    self._hostname=""
    dbg(f"config:{self.config.__dict__}")

    dbg(f"making dirs")
    ensure_dir(self.config.tmp_path)
    ensure_dir(self.config.screenshot_path)
    ensure_dir(self.config.ff_data_path)
    ensure_dir(self.config.ff_profile_path)

    # "proxy rotating"
    # sppoof - access geoblocked websites and hide IP addr
    # from selenium.webdriver.common.proxy import Proxy, ProxyType
    # myProxy = "xx.xx.xx.xx:xxxx"
    # proxy = Proxy({
    #     'proxyType': ProxyType.MANUAL,
    #     'httpProxy': myProxy,
    #     'ftpProxy': myProxy,
    #     'sslProxy': myProxy,
    #     'noProxy': '' # set this value as desired
    #     })

    #anti-bot stuff:    
    # #https://stackoverflow.com/questions/68895582/how-to-avoid-a-bot-detection-and-scrape-a-website-using-python
    #https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
    #firefox source code: https://hg.mozilla.org/mozilla-unified
    # see:#https://kb.mozillazine.org/About:config_entries
    #https://hg.mozilla.org/mozilla-unified/file/522fdb5b8cfdf47e8accbfb6438138b30e03ea9e/browser/app/profile/firefox.js

    dbg(f"making driver")
    self.create_driver()

    dbg(f"Configuring Bot")
    self.config_bot()

    quit()

    dbg(f"Loading Link Database")
    self.csv.load()

  def create_driver(self):
    options = webdriver.firefox.options.Options()
   # logfp=os.path.join(self.config.tmp_path, "out_log.txt")
   # logfp2=os.path.join(self.config.tmp_path, "out_log2.txt")
    #msg(f"log={logfp}")
   # fb = FirefoxBinary(log_file = sys.stdout) #logfp) 
   # options.binary = fb
    options.add_argument('-headless') #yes it is 1 dash see selenium firefox_binary.py
    #options.add_argument(f"-user-data-dir={self.config.ff_data_path}")

    # this causes issues
    #options.add_argument(f"-profile={self.config.ff_profile_path}")

    #https://stackoverflow.com/questions/34739969/webdriver-use-firefox-developer-tools-in-selenium-test-case
    #options.set_preference("devtools.netmonitor.enabled",True)
    #options.set_preference("devtools.netmonitor.har.compress",False)

    #os.environ["MOZ_REMOTE_SETTINGS_DEVTOOLS"] = "1"
    #options.set_preference("services.settings.loglevel", "debug")#??
    options.set_preference("browser.aboutConfig.showWarning", False)
    #options.log.level = "info" # "trace" #https://firefox-source-docs.mozilla.org/testing/geckodriver/TraceLogs.html
    #self.service = Service(log_path = sys.stdin)
    self.driver = webdriver.Firefox(options=options)

    #default_ua = self.driver.execute_script('return navigator.webdriver')
    #dbg(f"Default User-Agent:{default_ua}")

  def config_bot(self):
    self.driver.get("about:config")
    self.random_agent()
    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    #self.driver.execute_script("Object.defineProperty(navigator, 'webDriver', {get: () => undefined})")

    self.test_bot_config()

    winx = make_fuzzy([0, 240, 1920])
    winy = make_fuzzy([0, 140, 3840])
    self.driver.set_window_size(winx, winy)

  def _raw_execjs(self, src):
    r = self.driver.execute_script(src)
    return r

  def print_js_src(self, src_raw, ln = 0, l_c = 0):
    src_ln=""
    lines = src_raw.splitlines()
    l_b = max(0, ln - l_c)
    l_e = (len(lines) if l_c == 0 else min(ln + l_c, len(lines)))
    for i in range(l_b, l_e):
      line = lines[i]
      lns=f"{i}".ljust(5)
      if i == ln:
        src_ln += f"{logcol.yellowb}{lns} {logcol.blueb}{line}\n"
      else:
        src_ln += f"{logcol.yellow}{lns} {logcol.blue}{line}\n"

    print(f"{src_ln}")

  def execjs(self, src):
    r = self._raw_execjs(src)

    (log, ex) = self.get_js_log()
    if log != "":
      if ex != None:
        (ln, lc) = (0,-1) if ex == '-1' else (ex,6)
        self.print_js_src(src, ln, lc)
      print(log)

    return r

  def safe_execjs(self, src):
    r=""
    src= """
      ___ret = ""
      try { 
        ___ret = (function (){ 
          """+src+""" 
        })();
      } 
      catch(e) {
        window.console.except(e)
      };
      return ___ret;
      """
    try:
      r = self.execjs(src)
    except Exception as e:
      #dbg(f"{dir(e)}")
      err(f"{e.msg}")
     # err(f"{src}")
      #printExcept(e)      
    except:
      err("Unkown exception caught")

    return r    
  
  def get_js_log(self):
    logjsonstr = self._raw_execjs("return window.window.get_selenium_log()")
    #dbg(f"logjsonstr={logjsonstr}")
    logjson = json.loads(logjsonstr)
    st=""
    ex=None
    for ls in logjson:
      st += "js: "
      if ls['tag'] == 'debug':
        st += f"{logcol.blueb}debug "
      elif ls['tag'] == 'error':
        st += f"{logcol.redb}error "
      elif ls['tag'] == 'info':
        st += f"{logcol.white}info  "
      else:
        ex = int(ls['ln'])
        st += f"{logcol.whiteb}{ls['tag']} "

      if ls['fn'] != '' or ls['ln'] != '':
        if ls['fn'] == '':
          fn="<no-file>"
        else:
          fn=ls['fn']
        if ls['ln'] == '':
          ln="<no-line>"
        else:
          ln=ls['ln']          
        st += f"{logcol.greenb}{fn}:{logcol.yellowb}{ln}"
      st += " " 

      st += f" {logcol.blueb}{ls['msg']}{logcol.reset}\n"
    return (st, ex)


  def initjs(self):
    #init js comm
    
    self._raw_execjs("""
    //import { load } from '../BotD/dist/botd.esm.js'
    //import('https://requirejs.org/docs/release/2.3.6/minified/require.js')

    """)
    self._raw_execjs("""
      window.selenium_log = []
    """)
    self._raw_execjs("""
      window.log_selenium = function (msg, tag, fn="", ln=-1) {
        window.selenium_log.push({fn: "" + fn, tag:"" + tag, ln:(ln===-1 ? "" : "" + ln), msg: "" + msg})
      }
    """)
    self._raw_execjs("""
      window.console.log = (msg) => { window.log_selenium(msg,"info") }
      window.console.error = (msg) => { window.log_selenium(msg,"error") }
      window.console.except = (e) => { window.log_selenium(e.message, e.name, e.fileName, e.lineNumber) }
      window.console.debug = (msg) => { window.log_selenium(msg,"debug") }
      //window.onerror = function (msg, url, line) {
      //  window.log_selenium(msg,"exception",url,line)
      //  return false; //true; // avoid to display an error message in the browser
      //}
    """)
    self._raw_execjs("""
      window.get_selenium_log = function() {
        logstr = JSON.stringify(window.selenium_log)
        window.selenium_log=[]
        return logstr
      }
    """)
    self._raw_execjs("""
      console.log("Initializing selenium aitools js")
    """)
  def test_bot_config(self):
    #redirect log
    self.driver.get('https://www.scrapethissite.com/pages/advanced/?gotcha=headers')
    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    self.initjs()


    # userAgent: getUserAgent,
    # appVersion: getAppVersion,
    # rtt: getRTT,
    # windowSize: getWindowSize,
    # pluginsLength: getPluginsLength,
    # pluginsArray: getPluginsArray,
    # errorTrace: getErrorTrace,
    # productSub: getProductSub,
    # windowExternal: getWindowExternal,
    # mimeTypesConsistent: areMimeTypesConsistent,
    # evalLength: getEvalLength,
    # webGL: getWebGL,
    # webDriver: getWebDriver,
    # languages: getLanguages,
    # notificationPermissions: getNotificationPermissions,
    # documentElementKeys: getDocumentElementKeys,
    # functionBind: getFunctionBind,
    # process: getProcess,
    # distinctiveProps: checkDistinctiveProperties,

    #TODO: other BotD stuff
    dbg(f"  navigator.userAgent: {self.execjs('return navigator.userAgent')}")
    dbg(f"  document.documentElement: {self.execjs('return document.documentElement')}")
    dbg(f"  navigator.appVersion: {self.execjs('return navigator.appVersion')}")
    dbg(f"  navigator.webDriver: {self.execjs('return navigator.webDriver')}")
    dbg(f"  navigator.webdriver: {self.execjs('return navigator.webdriver')}")
    dbg(f"  navigator.languages: {self.execjs('return navigator.languages')}")
    dbg(f"  navigator.permissions: {self.execjs('return navigator.permissions')}")
    dbg(f"  eval.tostring: {self.execjs('return eval.toString()')}")
    dbg(f"  evalLength: {self.execjs('return eval.toString().length')}")

    be="""
    function countTruthy(values) {
      return values.reduce(function (sum, value) { return sum + (value ? 1 : 0); }, 0);
    }
    function getBrowserEngineKind() {
        var _a, _b;
        // Based on research in October 2020. Tested to detect Chromium 42-86.
        var w = window;
        var n = navigator;
        if (countTruthy([
            'webkitPersistentStorage' in n,
            'webkitTemporaryStorage' in n,
            n.vendor.indexOf('Google') === 0,
            'webkitResolveLocalFileSystemURL' in w,
            'BatteryManager' in w,
            'webkitMediaStream' in w,
            'webkitSpeechGrammar' in w,
        ]) >= 5) {
            return 'BrowserEngineKind.Chromium';
        }
        if (countTruthy([
            'ApplePayError' in w,
            'CSSPrimitiveValue' in w,
            'Counter' in w,
            n.vendor.indexOf('Apple') === 0,
            'getStorageUpdates' in n,
            'WebKitMediaKeys' in w,
        ]) >= 4) {
            return 'BrowserEngineKind.Webkit';
        }
        if (countTruthy([
            'buildID' in navigator,
            'MozAppearance' in ((_b = (_a = document.documentElement) === null || _a === void 0 ? void 0 : _a.style) !== null && _b !== void 0 ? _b : {}),
            'onmozfullscreenchange' in w,
            'mozInnerScreenX' in w,
            'CSSMozDocumentRule' in w,
            'CanvasCaptureMediaStream' in w,
        ]) >= 4) {
            return 'BrowserEngineKind.Gecko';
        }
        return BrowserEngineKind.Unknown;
    }
    """

    # browserified botd    
    #https://stackoverflow.com/questions/22710887/compile-an-npm-module-into-a-single-file-without-dependencies
    #  npx browserify -s botd --bare ./dist/botd.cjs.js -o botd2.js
    #botd_src += Utils.read_file_string("./require.js")
    botd_src = """
    """+Utils.read_file_string("./botd2.js")+"""
    //const botdPromise = import('https://openfpcdn.io/botd/v1').then((Botd) => Botd.load())
    
    window.botd.load()
      .then((botd) => botd.detect())
      .then((result) => console.log("botd res="+JSON.stringify(result)))
      .catch((error) => console.error("botd err="+error))
    
    """

    self.safe_execjs(botd_src);

    time.sleep(1) 
    self.safe_execjs("console.log('logging shit')");
    self.get_js_log()

    quit()

  def random_agent(self):
    dbg(f" Reconfiguring:")
    ua = UserAgent()
    new_ua = ua.random
    self.driver.execute_script(f"Services.prefs.setStringPref('general.useragent.override', '{new_ua}');")

  def save_html_to_file(self):
    html_fn = re.sub(r'[^\w_. -]', '_', self.driver.current_url) + ".html"
    html_file = os.path.join(self.config.html_path, html_fn)
    dbg(f"html_file={html_file}")
    ensure_dir(self.config.html_path)
    with open(html_file, 'w') as f:
      f.write(self.driver.page_source)

  def scrape(self):
    #begin with base link
    self._next.append(self.get_link(self.config.base_url))
    try:
      #TODO: async and also recursive
      # while len(self._next): # or parse time
      link = self._next[0]
      self._next.remove(link)
      self.visit(link)
      
      st = make_fuzzy(self.config.visit_delay)
      dbg(f"sleeping for {st}s")
      time.sleep(st) 

    except Exception as e:
      Utils.printExcept(e)
      self.shutdown()

  def visit(self, html_link:Link):
    try:
      dbg(f"request url={html_link.url}")
      #response = self.driver.execute("get", {"url": html_link.url})
      self.driver.get(html_link.url)

      time.sleep(1) 

      page_url = self.driver.current_url
      dbg(f"respose url={page_url}")
      self._hostname = urlparse(self.driver.current_url).hostname

      #page_url.replace()
      #pathname2url(page_url)
      #debug:save page source
      #dbg(f"response={response}")

      self.save_html_to_file()

      #save jpgot
      ss_path = os.path.join(self.config.screenshot_path, f"ss-{millis()}.jpg")
      dbg(f"saving ss: {ss_path}")
      self.driver.save_screenshot(ss_path)

      # TODO
      # TODO
      # TODO
      # TODO
      # TODO
      #if r == 200: 
      #  self.process_page()
      #else:
      #  err(f"URL {html_link.url} returend error code {r.status_code}")
      #  trap()
    except Exception as e :
      err(f"Request failed '{html_link.url}'")
      raise e
  
  def process_page(self):
    #must check if page is scrollable scroll then be done after some condition
    self._link_tags={}
    visit_start = datetime.now()
    (wx, wy) = driver.get_size()
    self._page_height = wy
    dbg(f"#src={len(driver.page_source)}")
    
    while True:
      self.scrape_media()
      time.sleep(self.config.scroll_delay_s + random.uniform(self.config.scroll_delay_random_i_s, self.config.scroll_delay_random_a_s)) 
      body = driver.find_element(By.XPATH, "//body")
      
      body.sendKeys(Keys.PAGE_DOWN);
      #new_height = driver.execute_script('return document.body.scrollHeight') 
      
        

      #TODO: we need to check the http requests in driver to see if stuff is still loading

      if (datetime.now()-visit_start).total_seconds() >= self.config.visit_time_s:
        break
      elif new_height == self._page_height: #may need to be fuzzy here 
        break 
      else:
        self._page_height = new_height 

  def check_thumbnail(self, link, tag):
    if tag.parent.name == 'a':
      # get top of tag    
      dbg(f"tag.innerText={tag.innerText}")
      tagstr = re.match("^<.*>", tag.innerText)
      dbg(f"tagstr={tagstr}")
      tag_hash = hash(tagstr)
      self._link_tags[tag_hash] = tag
      #google parent <a> is actually a button, we ned to execute the JS
      #href = tag.parent.get('href') #TODO: may have to "search"
      ##if href == None:
      #  href = tag.parent.get('href') 
      #  if href == None:
       #   dbg("img tag or too small")

  def scrape_media(self):
    tag_names={'img':['.jpg','.jpeg','.png','.gif'],'video':['.mp4','.mpg','.avi','.ts']}
    for tn,tt in tag_names:
      tags = driver.find_elements(By.TAG_NAME, tn); 
      dbg(f"#tags={len(tags)}")
      for tag in tags:
        self.save_media(tag, tt)

  def find_actual_source(self, tag):
    #coudl be thumb, or parent etc.
    #find ancestral <a>
    href=""
    if tag.parent.name == 'a':
      href = tag.parent.get('href') 
    if href == None and tag.parent.parent.name == 'a':
      href = tag.parent.parent.get('href') 
    if href == None and tag.parent.parent.parent.name == 'a':
      href = tag.parent.parent.parent.get('href') 

    if href and len(href):
      dbg("appending parent")
      parentlink = self.get_link(href)
      self._next.append(parentlink)

  def save_media(self, tag, tt):
    if tag:
      if tag.is_displayed(): #only download displayed tags to prevent browser from detecting a bot
        src_raw = tag.get_attribute('src')
        src = self.format_src(src_raw)
        if src:
          dbg(f"tagurl:{src}")
          link = self.get_link(src)
          srcpath = urlparse(src).path
          ext = os.path.splitext(srcpath)
          if ext in tt:
            diff_s = (link.last_query - datetime.now()).total_seconds()
            if link.last_query == datetime.min or diff_s > self.config.link_query_delay_s:
              if self.filter_media(tag):
                #save
                fname = os.path.basename(urlpath)
                path = os.path.abspath(os.path.join(self.config.img_path, fname))
                dbg(f"img {fname}")
                dbg(f" SAVING path {path}")
                link._data.save(path)
                dbg(f"   -> {url}")
        else:
          dbg(f"no src for '{tag}'")
      else:
        dbg(f"tag '{tag}' not displayed")
    else:
      err(f"URL '{tag}' was none")

  def filter_media(link):
    w,h = link.get_size(tag)
    if w>=self.config.img_min_w and h>=self.config.img_min_h:
      link.status = LinkStatus.TooSmall
    else:
      link.status = LinkStatus.Success

  def load_img(self, link) -> bool:
    with urllib.request.urlopen(link.url) as u:
      f = BytesIO(u.read())
      link._data = Image.open(f)
      return link._data != None
    
  def get_img_size(self, link, tag) -> tuple:
   # s=tag.size()
    w = tag.value_of_css_property('width')
    h = tag.value_of_css_property('height')
    #   w=tag.get_attribute('width')
    #h=tag.get_attribute('height')
    #get_dom_attribute
    if w and h:
      return (int(w),int(h))
    else:
      if link._data is None:
        self.load()
      if link._data is Image:
        return (link._data.width, link._data.height)
    return (0, 0)

  def format_src(src_url):
    url=src_url
    if url.startswith("/"):
      url=self._hostname+url
      dbg(f"url:{url}")
    if "http://" not in url and "https://" not in url:
      url = "http://" + url
    return url
  
  def get_link(self, url:str):
    if not url:
      trap()
    url_hsh = hash(url)
    if url_hsh not in self.img_links.keys():
      link = Link()
      link.url = url
      self.img_links[url_hsh] = link
    else:
      link = self.img_links[url_hsh]
    return link


with WebScraper() as ws:
  ws.scrape()

#   #def run_gecko_spider():
#   #https://github.com/SeleniumHQ/selenium/blob/trunk/py/selenium/webdriver/common/options.py
#   #https://www.selenium.dev/documentation/webdriver/elements/finders/

# # s = WebScraper()
# # s.scrape()

# #run_gecko_spider()
# #run_scrapy_spider()

# def scarpy_example():
#   #https://stackoverflow.com/questions/61859239/scrapy-parse-webpage-extract-results-pages-and-download-images

#   class MySpider(scrapy.Spider):
#     name = 'myspider'

#     #allowed_domains = []
#     #https://www.google.com/search?q=ass
#     start_urls = ['https://www.google.com/search?q=ass']

#     def parse(self, response):
#       print('url:', response.url)
#       #url= response.css("body div.site-container div#container div.ml_containermain div.content-helper div.aside-site-content div.product form#product_form_83013851 div.product-gallery div#product_images_83013851_update div.slide a#det_img_link_83013851_25781870")
#       #yield ImgData(image_urls=[url.xpath('@href').extract_first()])
#       # download files (not only images, but without converting to JPG)
#       #hxs = HtmlXPathSelector(response)
#       sel=Selector(response)
#       images = sel.xpath("//div[@id='ires']//div//a[@href]").extract()

#       #images = hxs.select("//div[@id='ires']//div//a[@href]")
#       dbg(f"images={images}")
#       # for url in response.css('img::attr(src)').extract():
#       #   url = response.urljoin(url)
#       #   yield {'file_urls': [url]}

#   c = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0',

#     # save in file CSV, JSON or XML
#     #'FEED_FORMAT': 'csv',     # csv, json, xml
#     #'FEED_URI': 'output.csv', #

#     # used standard FilesPipeline (download to FILES_STORE/full)
#     'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},  

#     # this folder has to exist before downloading
#     'FILES_STORE': './et',                   
#   })
#   c.crawl(MySpider)
#   c.start()

# scarpy_example()


# # url= response.css("body div.site-container div#container div.ml_containermain div.content-helper div.aside-site-content div.product form#product_form_83013851 div.product-gallery div#product_images_83013851_update div.slide a#det_img_link_83013851_25781870")
# # yield ImgData(image_urls=[url.xpath('@href').extract_first()])

# #r = requests.get(html_link.url)
# #driver.get(html_link.url)
# #https://github.com/SeleniumHQ/selenium/blob/trunk/py/selenium/webdriver/remote/command.py
# '''
# clickable = driver.find_element(By.ID, "clickable")
# ActionChains(driver)\
#     .click_and_hold(clickable)\
#     .perform()
#     pass that information to the browser with --window-size.

#     The default window size and display size in headless mode is 800x600 on all platforms.

#   action = ActionBuilder(driver)
#   action.pointer_action.move_to_location(8, 0)
#   action.perform()

#   scroll_origin = ScrollOrigin.from_viewport(10, 10)

#   ActionChains(driver)\
#       .scroll_from_origin(scroll_origin, 0, 200)\
#       .perform()
# '''
# #it needs to run in the background or something
# #the javascript is definitely delayed.
#   #
#   #
#   scroll_origin = ScrollOrigin.from_viewport(10, 10)

#   ActionChains(driver)\
#       .scroll_from_origin(scroll_origin, 0, 200)\
#       .perform()
# #   tags = driver.find_elements(By.TAG_NAME, "img"); #List[WebElement{
#   # dbg(f"{driver.page_source}")
#   #(link.last_query - datetime.now()).total_seconds()

# #https://github.com/SeleniumHQ/selenium/blob/trunk/py/selenium/webdriver/remote/webelement.py
#   # dbg(f"got tags:{len(tags)}")
  

#   #By.cssSelector("img")
#   #tag.location_once_scrolled_into_view ** OOH cool 

# #https://github.com/SeleniumHQ/selenium/blob/trunk/py/selenium/webdriver/remote/webdriver.py
# # value_element = WebDriverWait(driver, 10).until(
# #     EC.text_to_be_present_in_element_value((By.ID, "share-tradingdata-o"))
# # )

# # element = WebDriverWait(browser, 10).until(
# #     EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[13]/div/div[2]/div/p"))
# # )
# #https://stackoverflow.com/questions/62271849/the-selenium-webdriver-returns-none-when-scraping-the-web-page-for-dynamic-numbe


# # def import_selenium():
# #   from selenium import webdriver
# #   from selenium.webdriver.common.by import By
# #   from selenium.webdriver.support.ui import WebDriverWait
# #   from selenium.webdriver.support import expected_conditions as EC

# # def import_soup():
# #   import bs4 as bs

# # def import_scrapy():
# #   #https://docs.scrapy.org/en/latest/
# #   import scrapy

# # def setup_imports()->None:
# #   try:
# #     import_scrapy()
# #   except ImportError:
# #       msg("failed to import scrapy trying selenium")
# #       try:
# #         import_selenium()
# #       except ImportError:
# #         msg("failed to import selenium trying soup")
# #         try:
# #           import_soup()
# #         except ImportError:
# #           err_exit("failed to import either API")



#https://www.zenrows.com/blog/dynamic-web-pages-scraping-python#infinite-scroll-pages

#from selenium.webdriver.chrome.service import Service as ChromeService 
#from webdriver_manager.chrome import ChromeDriverManager 
 #service=ChromeService(ChromeDriverManager().install()), options=options
# options = webdriver.FirefoxOptions() 
# options.headless = True 
# driver = webdriver.Firefox() 


#*this seems to work
# opts = webdriver.firefox.options.Options()
# opts.add_argument('-headless')
# #opts.add_argument('--window-size=1920,1080')
# driver = webdriver.Firefox(opts)
# #https://scrapingclub.com/exercise/list_infinite_scroll/
# url = 'https://www.google.com/search?q=ass' 
# driver.get(url) 
# items = [] 
# last_height = driver.execute_script('return document.body.scrollHeight') 
# itemTargetCount = 20 
# # scroll to bottom of webpage 
# while itemTargetCount > len(items): 
#   driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
#  # so = ScrollOrigin.from_viewport(10, 10)
#   #ActionChains(driver).scroll_from_origin(so, 0, 200).perform()
#   tags = driver.find_elements(By.TAG_NAME, "img"); #List[WebElement{
#   #elements = driver.find_elements(By.XPATH, "//div[@class='card-body']/h4/a") 
#   dbg(f"#src={len(driver.page_source)}")
#   dbg(f"#tags={len(tags)}")
#   for t in tags:
#     dbg(f"url:{t.get_attribute('src')}")

    # if api == SpiderAPI.BeautifulSoup:
    #   opener = urllib.request.build_opener()
    #   opener.add_headers = [{'User-Agent':'Mozilla'}]
    #   urllib.request.install_opener(opener)      
    # elif api == SpiderAPI.Selenium:
    # elif api == SpiderAPI.Scrapy:
    #   pass
#   time.sleep(1) 

#   # we need to check the requests

#   new_height = driver.execute_script('return document.body.scrollHeight') 
 
#   if new_height == last_height: 
#     break 
 
#   last_height == new_height 

# import response
# response = requests.post('https://ms-mt--api-web.spain.advgo.net/search', headers=headers, data=data).json()
    