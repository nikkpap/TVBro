"""TVBro 1.0 — Nick Paridis. Python 3.10+, PySide6, python-vlc, VLC 3.x."""
from __future__ import annotations
import os, sys, re, json, time, base64, zlib, shutil, tempfile, threading, struct, hashlib
import urllib.request, urllib.parse, urllib.error
from pathlib import Path
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import xml.etree.ElementTree as ET

VERSION = '1.4.1'
DEFAULT_PLAYLIST = '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'
UA = 'Mozilla/5.0 GreekTVPlayer/1.0'

@dataclass
class Source:
    url: str
    headers: dict = field(default_factory=dict)
    state: str = 'pending'
    reason: str = 'Δεν ελέγχθηκε'
    metadata: dict = field(default_factory=dict)
    checked_at: float = 0.0

@dataclass
class Channel:
    key: str
    name: str
    group: str
    logo: str = ''
    sources: list = field(default_factory=list)
    @property
    def state(self):
        if any(s.state == 'online' for s in self.sources): return 'online'
        if all(s.state == 'offline' for s in self.sources): return 'offline'
        return 'pending'


def parse_m3u(text):
    channels = {}; attrs = {}; name = ''; headers = {}; group = ''
    for raw in text.lstrip('\ufeff').splitlines():
        line = raw.strip()
        if not line: continue
        if line.startswith('#EXTINF:'):
            # Find the title delimiter outside quoted metadata (commas may occur inside attributes).
            quoted = False; split = -1
            for i, c in enumerate(line):
                if c == '"': quoted = not quoted
                elif c == ',' and not quoted: split = i; break
            meta = line[:split] if split >= 0 else line
            name = line[split+1:].strip() if split >= 0 else 'Channel'
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', meta)); headers = {}; group = attrs.get('group-title', '')
        elif line.startswith('#EXTGRP:'): group = line[8:].strip()
        elif line.startswith('#EXTVLCOPT:'):
            k, _, v = line[11:].partition('=')
            if k == 'http-referrer': headers['Referer'] = v
            elif k == 'http-user-agent': headers['User-Agent'] = v
        elif line.startswith('#'): continue
        else:
            url, _, suffix = line.partition('|')
            if urllib.parse.urlsplit(url).scheme not in ('http','https','rtsp','rtmp','udp','rtp'): continue
            for k, v in urllib.parse.parse_qsl(suffix):
                if k.lower() in ('user-agent','referer','origin','cookie','authorization'): headers[k.title()] = v
            clean = re.sub(r'\s*\[Πηγή \d+\]$', '', attrs.get('tvg-name', name or url))
            key = attrs.get('tvg-id') or (group + '|' + clean.casefold())
            ch = channels.setdefault(key, Channel(key, clean, group or 'Χωρίς κατηγορία', attrs.get('tvg-logo','')))
            if not any(s.url == url and s.headers == headers for s in ch.sources): ch.sources.append(Source(url, dict(headers)))
            attrs = {}; name = ''; headers = {}; group = ''
    return list(channels.values())


def fetch(url, headers=None, limit=2_000_000, timeout=7, metadata=None):
    if urllib.parse.urlsplit(url).scheme not in ('http','https'): raise ValueError('HTTP/HTTPS required')
    req = urllib.request.Request(url, headers={'User-Agent': UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data=r.read(limit)
        if metadata is not None:
            metadata.clear()
            metadata.update({'etag':r.headers.get('ETag',''),'modified':r.headers.get('Last-Modified',''),'mime':r.headers.get('Content-Type',''),'prefix':hashlib.sha256(data[:2048]).hexdigest()})
        return data, r.geturl(), r.headers.get('Content-Type','')


def source_key(source):
    # Store only a fingerprint, never playlist URLs, Xtream passwords or cookies.
    return hashlib.sha256(json.dumps([source.url,source.headers],sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def check_plan(channels, disabled, now=None):
    now=time.time() if now is None else now
    jobs=[]
    for ci,ch in enumerate(channels):
        if ch.key in disabled:continue
        new=[i for i,s in enumerate(ch.sources) if s.state=='pending' or not s.checked_at]
        jobs.extend((ci,i,'full') for i in new)
        online=[i for i,s in enumerate(ch.sources) if s.state=='online' and i not in new]
        if online:jobs.append((ci,online[0],'quick'))
        elif not new:
            due=[i for i,s in enumerate(ch.sources) if now-s.checked_at>=300]
            # One source first; fallback is scheduled if it is still offline.
            if due:jobs.append((ci,due[0],'full'))
    return jobs


def quick_probe(source,cancel=None):
    if cancel and cancel.is_set():return 'pending','Ακυρώθηκε'
    if urllib.parse.urlsplit(source.url).scheme not in ('http','https'):return probe(source,cancel)
    old=dict(source.metadata);headers=dict(source.headers)
    if old.get('etag'):headers['If-None-Match']=old['etag']
    if old.get('modified'):headers['If-Modified-Since']=old['modified']
    try:
        new={};data,_,mime=fetch(source.url,headers,limit=2048,timeout=3.5,metadata=new)
        if not data:return 'offline','Γρήγορος έλεγχος: κενή απόκριση'
        if 'text/html' in mime:return 'offline','Γρήγορος έλεγχος: ιστοσελίδα αντί για stream'
        if new.get('prefix')==old.get('prefix'):
            source.metadata=new
            return 'online','Γρήγορος HTTP έλεγχος: ίδια πηγή / διαθέσιμη απόκριση'
        # Changed manifest/content: perform the normal media check only here.
        return probe(source,cancel)
    except urllib.error.HTTPError as e:
        if e.code==304:return 'online','Γρήγορος conditional έλεγχος: 304 / χωρίς αλλαγή'
        return 'offline',f'Γρήγορος έλεγχος: HTTP {e.code}'
    except Exception:
        return 'offline','Γρήγορος έλεγχος: timeout / μη διαθέσιμο'


def probe(source, cancel=None):
    """Reachability + HLS media sample; it is not a decoder or a proof of ongoing broadcast."""
    try:
        if urllib.parse.urlsplit(source.url).scheme not in ('http','https'):
            return 'offline', 'Το πρωτόκολλο χρειάζεται δοκιμή στο VLC'
        url = source.url
        for depth in range(4):
            if cancel and cancel.is_set(): return 'pending','Ακυρώθηκε'
            data, final, mime = fetch(url, source.headers, limit=196608,metadata=source.metadata if depth==0 else None)
            if not data: return 'offline','Κενή απόκριση'
            text = data.decode('utf-8-sig','replace').lstrip()
            if text.startswith('#EXTM3U'):
                entries = [s.strip() for s in text.splitlines() if s.strip() and not s.startswith('#')]
                if not entries: return 'offline','Playlist χωρίς segments'
                if '#EXT-X-STREAM-INF' in text:
                    url = urllib.parse.urljoin(final, entries[0]); continue
                if '#EXT-X-KEY' in text and ('SAMPLE-AES' in text or 'KEYFORMAT=' in text):
                    return 'offline','DRM / προστατευμένη ροή'
                segment = urllib.parse.urljoin(final, entries[-1])
                chunk, _, segment_mime = fetch(segment, source.headers, limit=32768)
                if not chunk or 'text/html' in segment_mime: return 'offline','Το media segment δεν είναι διαθέσιμο'
                return 'online','HLS manifest και media segment διαθέσιμα'
            if '<MPD' in text or 'dash+xml' in mime:
                root = ET.fromstring(data)
                if any(x.tag.endswith('ContentProtection') for x in root.iter()): return 'offline','DRM / προστατευμένο DASH'
                if not any(x.tag.endswith('Representation') for x in root.iter()): return 'offline','DASH χωρίς Representation'
                return 'online','DASH manifest διαθέσιμο — επιβεβαίωση εικόνας στο VLC'
            if ('text/html' in mime or text[:40].lower().startswith(('<html','<!doctype','{"error'))):
                return 'offline','Επιστρέφει ιστοσελίδα ή σφάλμα αντί για βίντεο'
            is_ts = any(i+188 < len(data) and data[i] == 0x47 and data[i+188] == 0x47 for i in range(min(188,len(data))))
            if is_ts or data.startswith(b'FLV') or (len(data)>12 and data[4:8] in (b'ftyp',b'styp',b'moof')) or mime.startswith(('video/','audio/')):
                return 'online','Media bytes διαθέσιμα'
            return 'offline','Δεν αναγνωρίστηκε stream'
        return 'offline','Πολλά επίπεδα playlist'
    except urllib.error.HTTPError as e: return 'offline',f'HTTP {e.code}'
    except Exception as e: return 'offline',type(e).__name__ + ' / timeout ή μη διαθέσιμο'


def recording_format(source,preference='Auto',codecs=()):
    webm=urllib.parse.urlsplit(source.url).path.lower().endswith('.webm') or 'webm' in source.metadata.get('mime','').lower()
    flexible=any(str(codec).lower() in ('vp80','vp90','vp8','vp9','av01','av1','opus','vorb','vorbis') for codec in codecs)
    if preference=='MKV' or (preference=='Auto' and (webm or flexible)):
        return '.mkv','avformat{mux=matroska}'
    return '.ts','ts'


def recording_valid(path):
    try:
        with Path(path).open('rb') as f:data=f.read(1024)
        if len(data)<188:return False
        if Path(path).suffix.lower()=='.mkv':return data.startswith(bytes.fromhex('1a45dfa3'))
        return any(i+188<len(data) and data[i]==0x47 and data[i+188]==0x47 for i in range(min(len(data),188)))
    except OSError:return False


def xtream_channels(server, username, password):
    base = server.strip().rstrip('/')
    if '://' not in base: base = 'http://' + base
    if urllib.parse.urlsplit(base).scheme not in ('http','https'): raise ValueError('Μη έγκυρος server')
    query = urllib.parse.urlencode({'username':username,'password':password})
    def api(action=''):
        data,_,_=fetch(base+'/player_api.php?'+query+('&action='+action if action else ''),limit=24_000_000,timeout=20)
        return json.loads(data)
    auth = api()
    if str(auth.get('user_info',{}).get('auth','0')) != '1': raise ValueError('Αποτυχία σύνδεσης Xtream')
    categories = {str(c['category_id']):c['category_name'] for c in api('get_live_categories')}
    user = urllib.parse.quote(username,safe=''); pwd = urllib.parse.quote(password,safe='')
    result = []
    for c in api('get_live_streams'):
        sid = str(c['stream_id'])
        if not sid.isdigit(): continue
        ch = Channel('xc:'+__import__('hashlib').sha256(base.encode()).hexdigest()[:12]+':'+sid,str(c.get('name',sid)),categories.get(str(c.get('category_id')),'Live TV'),c.get('stream_icon',''))
        # Keep MPEG-TS first: most providers support it and VLC can record it directly.
        ch.sources = [Source(f'{base}/live/{user}/{pwd}/{sid}.ts'),Source(f'{base}/live/{user}/{pwd}/{sid}.m3u8')]
        result.append(ch)
    return result


# Bootstrap only UI dependencies. VLC itself must be installed separately with matching architecture.
def bootstrap():
    if os.name != 'nt':
        import PySide6, vlc
        return
    import importlib.util, subprocess, ctypes, hashlib, zipfile, queue
    import tkinter as tk
    from tkinter import ttk
    root_dir = Path(os.environ.get('LOCALAPPDATA',Path.home()))/'GreekTVPlayer'
    root_dir.mkdir(parents=True,exist_ok=True)
    # Hold a native single-instance lock during setup as well as playback.
    import msvcrt
    global setup_lock
    setup_lock = (root_dir/'setup.lock').open('a+b')
    setup_lock.seek(0);setup_lock.write(b'0');setup_lock.flush();setup_lock.seek(0)
    try:msvcrt.locking(setup_lock.fileno(),msvcrt.LK_NBLCK,1)
    except OSError:
        ctypes.windll.user32.MessageBoxW(None,'Η εφαρμογή εκτελείται ήδη.','TVBro',64);sys.exit(0)
    bits = 'win64' if struct.calcsize('P')==8 else 'win32'
    def matches(folder):
        dll=folder/'libvlc.dll'
        try:
            data=dll.read_bytes();pe=struct.unpack_from('<I',data,0x3c)[0];machine=struct.unpack_from('<H',data,pe+4)[0]
            return machine==(0x8664 if bits=='win64' else 0x14c)
        except Exception:return False
    candidates=[Path(os.environ.get('VLC_HOME','__missing__')),root_dir/'runtime/VLC',Path(__file__).resolve().parent/'VLC']
    candidates += [Path(os.environ.get(k,''))/'VideoLAN/VLC' for k in ('PROGRAMFILES','PROGRAMFILES(X86)')]
    selected=next((v for v in candidates if matches(v)),None)
    missing=[name for name,mod in [('PySide6>=6.7,<7','PySide6'),('python-vlc>=3.0.21203,<4','vlc')] if not importlib.util.find_spec(mod)]
    ui=tk.Tk();ui.overrideredirect(True);ui.configure(bg='#101b2c');w,h=490,225;ui.geometry(f'{w}x{h}+{(ui.winfo_screenwidth()-w)//2}+{(ui.winfo_screenheight()-h)//2}')
    tk.Label(ui,text='TVBro — Your live TV buddy.',font=('Segoe UI',24,'bold'),bg='#101b2c',fg='#61ddd5').pack(pady=(28,10))
    tk.Label(ui,text='Nick Paridis • VLC powered',font=('Segoe UI',11),bg='#101b2c',fg='#90a2bc').pack()
    status=tk.Label(ui,text='Initializing…',font=('Segoe UI',11),bg='#101b2c',fg='white');status.pack(pady=16)
    bar=ttk.Progressbar(ui,mode='indeterminate',length=400);bar.pack();bar.start(12);ui.lift();ui.attributes('-topmost',True)
    messages=queue.Queue();outcome={}
    def work():
        nonlocal selected
        try:
            if missing:
                messages.put('Εγκατάσταση Python dependencies…')
                python=Path(sys.executable).with_name('python.exe')
                result=subprocess.run([str(python),'-m','pip','install',*(['--user'] if sys.prefix==sys.base_prefix else []),*missing],creationflags=0x08000000,capture_output=True)
                if result.returncode:raise RuntimeError('Αποτυχία pip. Έλεγξε Internet / Python / pip.')
            if selected is None:
                messages.put('Λήψη VLC portable από VideoLAN…')
                version='3.0.24';filename=f'vlc-{version}-{bits}.zip'
                base=f'https://download.videolan.org/pub/videolan/vlc/{version}/{bits}/'
                checksum=fetch(base+filename+'.sha256',timeout=25)[0].decode().split()[0].lower()
                if not re.fullmatch(r'[0-9a-f]{64}',checksum):raise RuntimeError('Invalid VLC checksum')
                stage=Path(tempfile.mkdtemp(prefix='GreekTV-setup-'));archive=stage/filename
                try:
                    digest=hashlib.sha256();total=0
                    with urllib.request.urlopen(base+filename,timeout=45) as response,archive.open('wb') as dst:
                        while True:
                            block=response.read(262144)
                            if not block:break
                            total+=len(block)
                            if total>200_000_000:raise RuntimeError('VLC download exceeds limit')
                            digest.update(block);dst.write(block);messages.put(f'Λήψη VLC… {total/1048576:.1f} MB')
                    if digest.hexdigest()!=checksum:raise RuntimeError('VLC checksum mismatch')
                    messages.put('Έλεγχος και προετοιμασία VLC…')
                    unpack=stage/'unpack';unpack.mkdir()
                    with zipfile.ZipFile(archive) as z:
                        if sum(x.file_size for x in z.infolist())>700_000_000:raise RuntimeError('VLC archive exceeds limit')
                        for item in z.infolist():
                            target=(unpack/item.filename).resolve()
                            if not target.is_relative_to(unpack.resolve()):raise RuntimeError('Unsafe ZIP path')
                        z.extractall(unpack)
                    found=next(unpack.rglob('libvlc.dll')).parent
                    if not matches(found):raise RuntimeError('VLC architecture mismatch')
                    selected=root_dir/'runtime/VLC';selected.parent.mkdir(parents=True,exist_ok=True)
                    if selected.exists():shutil.rmtree(selected)
                    shutil.move(str(found),str(selected))
                finally:shutil.rmtree(stage,ignore_errors=True)
            os.environ['VLC_HOME']=str(selected);outcome['ok']=True;messages.put('Έτοιμο • άνοιγμα εφαρμογής…')
        except Exception as e:outcome['error']=str(e)
    thread=threading.Thread(target=work,daemon=True);thread.start();started=time.monotonic()
    def poll():
        latest=None
        while not messages.empty():latest=messages.get_nowait()
        if latest:status.configure(text=latest)
        if thread.is_alive() or time.monotonic()-started<1.6:ui.after(60,poll)
        else:ui.destroy()
    ui.after(60,poll);ui.mainloop()
    if 'error' in outcome:
        ctypes.windll.user32.MessageBoxW(None,outcome['error']+'\nΕκτέλεσε Install_Dependencies.bat ή εγκατάστησε VLC Desktop.','GreekTV Setup',16);sys.exit(1)


def launch():
    bootstrap()
    from PySide6.QtCore import Qt, QTimer, QThread, Signal, QUrl, QLockFile, QEvent, QTranslator, QLibraryInfo
    from PySide6.QtGui import QFont, QDesktopServices, QShortcut, QKeySequence, QColor, QIcon, QPixmap, QPainter, QCursor
    from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QListWidget,QListWidgetItem,QComboBox,QSlider,QSpinBox,QCheckBox,QFileDialog,QMessageBox,QInputDialog,QDialog,QFormLayout,QDialogButtonBox,QProgressBar,QMenu,QFrame,QSplitter,QTableWidget,QTableWidgetItem,QHeaderView)
    if os.name=='nt':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('NickParidis.TVBro.1')
    app = QApplication(sys.argv); app.setApplicationName('TVBro'); app.setFont(QFont('Segoe UI',10))
    icon=QPixmap(64,64);icon.fill(QColor('#147b8a'));painter=QPainter(icon);painter.setPen(QColor('#ffffff'));painter.setFont(QFont('Segoe UI',23,QFont.Weight.Bold));painter.drawText(icon.rect(),Qt.AlignmentFlag.AlignCenter,'TV');painter.end();app.setWindowIcon(QIcon(icon))
    dark_style='''
    QWidget { background: #0c111d; color: #e6edf8; }
    QMainWindow { background: #0c111d; } QLabel {background:transparent;}
    QScrollBar:vertical {background:#111b2c;width:8px;} QScrollBar::handle:vertical {background:#38506a;min-height:28px;border-radius:4px;} QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {height:0;}
    QLabel#brand {font-size:22px;font-weight:700;} QLabel#muted {color:#8495af;}
    QFrame#panel {background:#131c2c;border:1px solid #223049;border-radius:10px;}
    QPushButton {background:#1a263a;border:1px solid #2b3a52;border-radius:8px;padding:9px 13px;}
    QPushButton:hover {background:#273951;border-color:#56b6d9;}
    QPushButton:disabled {color:#4e607a;} QPushButton#primary {background:#147b8a;border-color:#229aa8;}
    QPushButton#ghost {background:transparent;border:1px solid #36445a;}
    QPushButton#record {color:#ff7f91;} QPushButton#record:checked {background:#74283a;color:white;}
    QLineEdit,QComboBox {background:#111b2c;border:1px solid #2b3a52;border-radius:7px;padding:8px;}
    QComboBox::drop-down {border:0;width:24px;background:transparent;}
    QListWidget {background:#101a2a;border:0;border-radius:8px;outline:0;}
    QListWidget::item {padding:9px;border-bottom:1px solid #1d2a40;}
    QListWidget::item:selected {background:#204656;color:#baf4fb;}
    QListWidget::item:hover {background:#1c2a3e;}
    QSlider::groove:horizontal {height:5px;background:#27384d;border-radius:2px;}
    QSlider::handle:horizontal {width:13px;margin:-4px 0;background:#60d1d2;border-radius:6px;}
    QProgressBar {border:0;background:#1c2a3e;border-radius:4px;text-align:center;max-height:15px;}
    QProgressBar::chunk {background:#279ba9;border-radius:4px;}
    QMenu {background:#132036;border:1px solid #34465e;padding:7px;}
    QMenu::item {padding:9px 20px;} QMenu::item:selected {background:#25455a;}
    QTableWidget {background:#111b2c;gridline-color:#29374c;} QHeaderView::section {background:#203048;padding:8px;border:0;}
    '''
    root = Path(os.environ.get('LOCALAPPDATA',Path.home()/'.local/share'))/'GreekTVPlayer'
    root.mkdir(parents=True,exist_ok=True)
    lock = QLockFile(str(root/'app.lock')); lock.setStaleLockTime(0)
    if not lock.tryLock(100):
        QMessageBox.information(None,'TVBro','Η εφαρμογή εκτελείται ήδη.'); return
    temp_root = Path(tempfile.gettempdir())/'GreekTVPlayer-session'
    # Only app-owned disposable directories are cleaned, never playlist files or recordings.
    for folder in (root/'cache',temp_root):
        if folder.is_symlink(): raise RuntimeError('Unsafe cache directory')
        if folder.exists(): shutil.rmtree(folder)
        folder.mkdir(parents=True)
    config_file = root/'settings.json'
    catalog_file = root/'catalog_status.json'
    try: settings = json.loads(config_file.read_text())
    except Exception: settings = {}
    os.environ['TMPDIR'] = str(temp_root)
    vlc_dir = None
    if os.name == 'nt':
        candidates = [Path(os.environ.get('VLC_HOME','__missing__')),Path(__file__).resolve().parent/'VLC']
        candidates += [Path(os.environ.get(k,''))/'VideoLAN/VLC' for k in ('PROGRAMFILES','PROGRAMFILES(X86)')]
        for folder in candidates:
            if (folder/'libvlc.dll').exists():
                vlc_dir = folder; os.environ['PATH']=str(folder)+os.pathsep+os.environ.get('PATH','')
                os.environ['VLC_PLUGIN_PATH']=str(folder/'plugins'); dll_handle=os.add_dll_directory(str(folder)); break
    demo = '--demo' in sys.argv
    try:
        import vlc
        engine = None if demo else vlc.Instance('--quiet','--ignore-config','--no-video-title-show','--no-media-library','--network-caching=1200','--no-video-on-top')
        if not demo and not engine: raise RuntimeError('VLC engine unavailable')
    except Exception:
        QMessageBox.critical(None,'VLC απαιτείται','Εγκατάστησε VLC Desktop ίδιας αρχιτεκτονικής με την Python (π.χ. και τα δύο 64-bit).\nhttps://www.videolan.org/vlc/\n\nΜετά άνοιξε ξανά την εφαρμογή.'); return

    light_style=dark_style
    for dark,light in {'#0c111d':'#f3f6fb','#e6edf8':'#162239','#8495af':'#586d86','#131c2c':'#ffffff','#223049':'#d5dfec','#1a263a':'#eaf0f7','#2b3a52':'#cfdae8','#273951':'#dce9f4','#4e607a':'#a4b1c2','#111b2c':'#ffffff','#101a2a':'#ffffff','#1d2a40':'#e5ecf5','#204656':'#d0eef1','#baf4fb':'#114b59','#1c2a3e':'#e6eef7','#27384d':'#cbd9e8','#132036':'#ffffff','#34465e':'#c5d3e4','#25455a':'#dcebf5','#29374c':'#dce5f0','#203048':'#e8eef6','#111b2c':'#ffffff','#38506a':'#a3b8cd'}.items():light_style=light_style.replace(dark,light)
    qt_translator=QTranslator(app)
    language=settings.get('language','GR')
    if language not in ('EN','GR','IT','FR','GER','RU','CH'):language='GR'
    translations={'Ρυθμίσεις': ['Settings', 'Impostazioni', 'Paramètres', 'Einstellungen', 'Настройки', '设置'], 'Θέμα εμφάνισης': ['Appearance', 'Aspetto', 'Apparence', 'Darstellung', 'Оформление', '外观'], 'Γλώσσα': ['Language', 'Lingua', 'Langue', 'Sprache', 'Язык', '语言'], 'Κλείσιμο': ['Close', 'Chiudi', 'Fermer', 'Schließen', 'Закрыть', '关闭'], 'Περισσότερες ρυθμίσεις…': ['More settings…', 'Altre impostazioni…', 'Plus de paramètres…', 'Weitere Einstellungen…', 'Другие настройки…', '更多设置…'], 'Αναζήτηση καναλιού…': ['Search channels…', 'Cerca canali…', 'Rechercher une chaîne…', 'Sender suchen…', 'Поиск каналов…', '搜索频道…'], 'Όλες οι κατηγορίες': ['All categories', 'Tutte le categorie', 'Toutes les catégories', 'Alle Kategorien', 'Все категории', '所有分类'], 'Όλα τα κανάλια': ['All channels', 'Tutti i canali', 'Toutes les chaînes', 'Alle Sender', 'Все каналы', '所有频道'], '★ Αγαπημένα': ['★ Favorites', '★ Preferiti', '★ Favoris', '★ Favoriten', '★ Избранное', '★ 收藏'], '↑ Move': ['↑ Move', '↑ Sposta', '↑ Monter', '↑ Nach oben', '↑ Вверх', '↑ 上移'], '↓ Move': ['↓ Move', '↓ Sposta', '↓ Descendre', '↓ Nach unten', '↓ Вниз', '↓ 下移'], 'Διακοπή': ['Cancel', 'Annulla', 'Annuler', 'Abbrechen', 'Отмена', '取消'], 'Έτοιμο': ['Ready', 'Pronto', 'Prêt', 'Bereit', 'Готово', '就绪'], 'Έλεγχος καναλιών': ['Checking channels', 'Verifica canali', 'Vérification des chaînes', 'Senderprüfung', 'Проверка каналов', '检查频道'], 'Ενσωματωμένη Greek TV': ['Built-in Greek TV', 'Greek TV integrata', 'Greek TV intégrée', 'Integriertes Greek TV', 'Встроенный Greek TV', '内置 Greek TV'], 'Greek TV • ενσωματωμένη λίστα': ['Greek TV • built-in playlist', 'Greek TV • lista integrata', 'Greek TV • liste intégrée', 'Greek TV • integrierte Liste', 'Greek TV • встроенный список', 'Greek TV • 内置列表'], 'Άνοιγμα M3U / M3U8…': ['Open M3U / M3U8…', 'Apri M3U / M3U8…', 'Ouvrir M3U / M3U8…', 'M3U / M3U8 öffnen…', 'Открыть M3U / M3U8…', '打开 M3U / M3U8…'], 'M3U από URL…': ['M3U from URL…', 'M3U da URL…', 'M3U depuis une URL…', 'M3U von URL…', 'M3U по URL…', '从 URL 加载 M3U…'], 'Xtream Codes…': ['Xtream Codes…', 'Xtream Codes…', 'Xtream Codes…', 'Xtream Codes…', 'Xtream Codes…', 'Xtream Codes…'], 'Όλες οι πηγές: ': ['Show all sources: ', 'Mostra tutte le sorgenti: ', 'Afficher toutes les sources : ', 'Alle Quellen anzeigen: ', 'Все источники: ', '显示所有来源：'], 'Διαχείριση ομάδων αγαπημένων': ['Manage favorite groups', 'Gestisci gruppi preferiti', 'Gérer les groupes favoris', 'Favoritengruppen verwalten', 'Управление группами', '管理收藏分组'], 'Κρυφά / Disabled κανάλια': ['Hidden / Disabled channels', 'Canali nascosti / disabilitati', 'Chaînes masquées / désactivées', 'Versteckte / deaktivierte Sender', 'Скрытые / отключённые каналы', '隐藏 / 禁用频道'], 'Εμφάνιση αγαπημένων': ['Show favorites', 'Mostra preferiti', 'Afficher les favoris', 'Favoriten anzeigen', 'Показать избранное', '显示收藏'], 'Φάκελος εγγραφών…': ['Recording folder…', 'Cartella registrazioni…', 'Dossier des enregistrements…', 'Aufnahmeordner…', 'Папка записей…', '录制文件夹…'], 'Άνοιγμα εγγραφών': ['Open recordings', 'Apri registrazioni', 'Ouvrir les enregistrements', 'Aufnahmen öffnen', 'Открыть записи', '打开录制文件'], 'Γρήγορος έλεγχος αλλαγών': ['Quick change check', 'Controllo rapido modifiche', 'Vérification rapide des changements', 'Schnelle Änderungsprüfung', 'Быстрая проверка изменений', '快速检查变化'], 'Πλήρης έλεγχος όλων': ['Full check of all sources', 'Controllo completo', 'Vérification complète', 'Alle Quellen vollständig prüfen', 'Полная проверка источников', '完整检查所有来源'], 'Πλήρης έλεγχος': ['Full check', 'Controllo completo', 'Vérification complète', 'Vollständige Prüfung', 'Полная проверка', '完整检查'], 'Πρώτος έλεγχος': ['Initial check', 'Primo controllo', 'Premier contrôle', 'Erste Prüfung', 'Первая проверка', '首次检查'], 'Info / κατάσταση καναλιών': ['Info / channel status', 'Info / stato canali', 'Infos / état des chaînes', 'Info / Senderstatus', 'Информация / статус каналов', '信息 / 频道状态'], 'Οδηγίες / About': ['Help / About', 'Guida / Informazioni', 'Aide / À propos', 'Hilfe / Über', 'Справка / О программе', '帮助 / 关于'], 'Διάλεξε κανάλι': ['Choose a channel', 'Scegli un canale', 'Choisir une chaîne', 'Sender auswählen', 'Выберите канал', '选择频道'], 'Διπλό κλικ σε διαθέσιμο κανάλι για αναπαραγωγή': ['Double-click an available channel to play', 'Doppio clic su un canale disponibile', 'Double-cliquez sur une chaîne disponible', 'Verfügbaren Sender doppelklicken', 'Дважды нажмите доступный канал', '双击可用频道播放'], 'Διαχείριση καναλιών': ['Channel management', 'Gestione canali', 'Gestion des chaînes', 'Senderverwaltung', 'Управление каналами', '频道管理'], 'Αναπαραγωγή': ['Play', 'Riproduci', 'Lire', 'Wiedergabe', 'Воспроизвести', '播放'], '↑ Μετακίνηση πάνω': ['↑ Move up', '↑ Sposta su', '↑ Monter', '↑ Nach oben', '↑ Вверх', '↑ 上移'], '↓ Μετακίνηση κάτω': ['↓ Move down', '↓ Sposta giù', '↓ Descendre', '↓ Nach unten', '↓ Вниз', '↓ 下移'], '★ Αγαπημένο': ['★ Favorite', '★ Preferito', '★ Favori', '★ Favorit', '★ Избранное', '★ 收藏'], 'Ομάδες αγαπημένων': ['Favorite groups', 'Gruppi preferiti', 'Groupes favoris', 'Favoritengruppen', 'Группы избранного', '收藏分组'], 'Νέα ομάδα…': ['New group…', 'Nuovo gruppo…', 'Nouveau groupe…', 'Neue Gruppe…', 'Новая группа…', '新分组…'], 'Νέα ομάδα': ['New group', 'Nuovo gruppo', 'Nouveau groupe', 'Neue Gruppe', 'Новая группа', '新分组'], 'Νέα ομάδα αγαπημένων': ['New favorite group', 'Nuovo gruppo preferiti', 'Nouveau groupe favori', 'Neue Favoritengruppe', 'Новая группа избранного', '新建收藏分组'], 'Όνομα ομάδας:': ['Group name:', 'Nome gruppo:', 'Nom du groupe :', 'Gruppenname:', 'Название группы:', '分组名称：'], 'Μετονομασία': ['Rename', 'Rinomina', 'Renommer', 'Umbenennen', 'Переименовать', '重命名'], 'Νέο όνομα:': ['New name:', 'Nuovo nome:', 'Nouveau nom :', 'Neuer Name:', 'Новое имя:', '新名称：'], 'Hide — απόκρυψη': ['Hide channel', 'Nascondi canale', 'Masquer la chaîne', 'Sender ausblenden', 'Скрыть канал', '隐藏频道'], 'Disable — απενεργοποίηση': ['Disable channel', 'Disabilita canale', 'Désactiver la chaîne', 'Sender deaktivieren', 'Отключить канал', '禁用频道'], 'Κρυφά / Disabled — επαναφορά': ['Hidden / Disabled — restore', 'Nascosti / disabilitati — ripristina', 'Masqués / désactivés — restaurer', 'Versteckt / deaktiviert — wiederherstellen', 'Скрытые / отключённые — восстановить', '隐藏 / 禁用 — 恢复'], 'Επαναφορά επιλεγμένων': ['Restore selected', 'Ripristina selezionati', 'Restaurer la sélection', 'Auswahl wiederherstellen', 'Восстановить выбранные', '恢复所选'], 'Δεξί κλικ σε κανάλι → Ομάδες αγαπημένων.': ['Right-click a channel → Favorite groups.', 'Clic destro sul canale → Gruppi preferiti.', 'Clic droit sur une chaîne → Groupes favoris.', 'Rechtsklick auf Sender → Favoritengruppen.', 'Правый клик по каналу → Группы избранного.', '右键频道 → 收藏分组。'], 'Κανάλι': ['Channel', 'Canale', 'Chaîne', 'Sender', 'Канал', '频道'], 'Κατηγορία': ['Category', 'Categoria', 'Catégorie', 'Kategorie', 'Категория', '分类'], 'Κατάσταση': ['Status', 'Stato', 'État', 'Status', 'Статус', '状态'], 'Πηγές / διάγνωση': ['Sources / diagnostics', 'Sorgenti / diagnosi', 'Sources / diagnostic', 'Quellen / Diagnose', 'Источники / диагностика', '来源 / 诊断'], 'Info • Κατάσταση καναλιών': ['Info • Channel status', 'Info • Stato canali', 'Infos • État des chaînes', 'Info • Senderstatus', 'Информация • Статус каналов', '信息 • 频道状态'], 'Φόρτωση λίστας': ['Load playlist', 'Carica lista', 'Charger la liste', 'Liste laden', 'Загрузить список', '加载播放列表'], 'Φόρτωση λίστας…': ['Loading playlist…', 'Caricamento lista…', 'Chargement de la liste…', 'Liste wird geladen…', 'Загрузка списка…', '正在加载播放列表…'], 'Σύνδεση…': ['Connecting…', 'Connessione…', 'Connexion…', 'Verbinden…', 'Подключение…', '正在连接…'], 'Αναπαραγωγή σταματημένη': ['Playback stopped', 'Riproduzione interrotta', 'Lecture arrêtée', 'Wiedergabe gestoppt', 'Воспроизведение остановлено', '播放已停止'], 'Επανασύνδεση στη ζωντανή ροή': ['Reconnecting to live stream', 'Riconnessione alla diretta', 'Reconnexion au direct', 'Verbindung zum Livestream', 'Повторное подключение к эфиру', '重新连接直播'], 'Πηγές καναλιού': ['Channel sources', 'Sorgenti canale', 'Sources de la chaîne', 'Senderquellen', 'Источники канала', '频道来源'], 'Φάκελος εγγραφών': ['Recording folder', 'Cartella registrazioni', 'Dossier des enregistrements', 'Aufnahmeordner', 'Папка записей', '录制文件夹'], 'Αποθηκευμένος έλεγχος': ['Saved check', 'Controllo salvato', 'Vérification enregistrée', 'Gespeicherte Prüfung', 'Сохранённая проверка', '已保存的检查'], 'Δεν ελέγχθηκε': ['Not checked', 'Non verificato', 'Non vérifié', 'Nicht geprüft', 'Не проверено', '未检查'], 'Δεν αποθηκεύτηκαν οι προτιμήσεις.': ['Preferences could not be saved.', 'Impossibile salvare le preferenze.', 'Impossible d’enregistrer les préférences.', 'Einstellungen konnten nicht gespeichert werden.', 'Не удалось сохранить настройки.', '无法保存设置。'], 'Δεν αποθηκεύτηκαν οι καταστάσεις καναλιών.': ['Channel states could not be saved.', 'Impossibile salvare gli stati dei canali.', 'Impossible d’enregistrer les états des chaînes.', 'Senderstatus konnte nicht gespeichert werden.', 'Не удалось сохранить статусы каналов.', '无法保存频道状态。'], 'κανάλια': ['channels', 'canali', 'chaînes', 'Sender', 'каналов', '个频道'], 'διαθέσιμα στη λίστα': ['available in the list', 'disponibili nella lista', 'disponibles dans la liste', 'in der Liste verfügbar', 'доступны в списке', '个可用频道'], 'πηγές ελέγχθηκαν.': ['sources checked.', 'sorgenti verificate.', 'sources vérifiées.', 'Quellen geprüft.', 'источников проверено.', '个来源已检查。'], 'οι υπόλοιπες κρατούν την τελευταία κατάσταση.': ['the others retain their last status.', 'le altre mantengono lo stato precedente.', 'les autres conservent leur dernier état.', 'die anderen behalten ihren letzten Status.', 'остальные сохраняют последний статус.', '其他来源保留上次状态。'], 'Οι υπόλοιπες κρατούν την τελευταία κατάσταση.': ['Other sources retain their last status.', 'Le altre sorgenti mantengono lo stato precedente.', 'Les autres sources conservent leur dernier état.', 'Andere Quellen behalten ihren letzten Status.', 'Остальные источники сохраняют последний статус.', '其他来源保留上次状态。'], 'Εφαρμογή IPTV με ενσωματωμένο VLC, M3U / Xtream Codes, έλεγχο πηγών, ομάδες αγαπημένων και εγγραφή ζωντανών ροών.': ['IPTV player with embedded VLC, M3U / Xtream Codes, source checks, favorite groups and live-stream recording.', 'Lettore IPTV con VLC integrato, M3U / Xtream Codes, verifica sorgenti, gruppi preferiti e registrazione delle dirette.', 'Lecteur IPTV avec VLC intégré, M3U / Xtream Codes, vérification des sources, groupes favoris et enregistrement du direct.', 'IPTV-Player mit integriertem VLC, M3U / Xtream Codes, Quellenprüfung, Favoritengruppen und Live-Aufnahme.', 'IPTV-плеер со встроенным VLC, M3U / Xtream Codes, проверкой источников, группами избранного и записью эфира.', '内置 VLC 的 IPTV 播放器，支持 M3U / Xtream Codes、来源检查、收藏分组和直播录制。'], 'Είμαστε ανοιχτοί σε συζητήσεις και ιδέες. Ένα δημόσιο brainstorming είναι καλύτερο από καθόλου brainstorming :) Στην υγειά μας!': ['Open for discussions and ideas. Public brainstorming is better than no brainstorming :) Cheers!', 'Aperti a discussioni e idee. Un brainstorming pubblico è meglio di nessun brainstorming :) Salute!', 'Ouverts aux discussions et aux idées. Un brainstorming public vaut mieux que pas de brainstorming :) Santé !', 'Offen für Diskussionen und Ideen. Öffentliches Brainstorming ist besser als keines :) Prost!', 'Открыты для обсуждений и идей. Публичный мозговой штурм лучше, чем его отсутствие :) Удачи!', '欢迎讨论和建议。公开集思广益总比没有更好 :) 干杯！'], 'Space: Pause • L: Go Live • R: REC • M: Mute • F: Fullscreen\nCtrl+B: Κανάλια • Ctrl+I: Info • Esc: Exit fullscreen\nREC επανασυνδέει τη ροή. Pause/seek εξαρτώνται από το stream.\nAuto-hide: χρόνος από τις Ρυθμίσεις, επιστροφή με κίνηση ποντικιού.': ['Space: Pause • L: Go Live • R: REC • M: Mute • F: Fullscreen\nCtrl+B: Channels • Ctrl+I: Info • Esc: Exit fullscreen\nREC reconnects the stream. Pause/seek depend on the stream.\nAuto-hide: 4 seconds; move the mouse to show controls.', 'Space: Pausa • L: Diretta • R: REC • M: Muto • F: Schermo intero\nCtrl+B: Canali • Ctrl+I: Info • Esc: Esci\nREC riconnette la diretta. Pausa/ricerca dipendono dalla sorgente.\nNascondi dopo 4 secondi; muovi il mouse per mostrare.', 'Space: Pause • L: Direct • R: REC • M: Muet • F: Plein écran\nCtrl+B: Chaînes • Ctrl+I: Info • Esc: Quitter\nREC reconnecte le flux. Pause/recherche dépendent du flux.\nMasquage après 4 secondes ; bougez la souris pour afficher.', 'Space: Pause • L: Live • R: REC • M: Stumm • F: Vollbild\nCtrl+B: Sender • Ctrl+I: Info • Esc: Beenden\nREC verbindet den Stream neu. Pause/Suche hängen vom Stream ab.\nNach 4 Sekunden ausblenden; Maus zum Einblenden bewegen.', 'Space: Пауза • L: Эфир • R: REC • M: Без звука • F: Полный экран\nCtrl+B: Каналы • Ctrl+I: Info • Esc: Выход\nREC переподключает поток. Пауза зависит от источника.\nСкрытие через 4 секунды; двигайте мышью для показа.', 'Space：暂停 • L：直播 • R：录制 • M：静音 • F：全屏\nCtrl+B：频道 • Ctrl+I：信息 • Esc：退出全屏\n录制会重新连接。暂停和跳转取决于直播源。\n4 秒后隐藏；移动鼠标即可显示。']}
    translations.update({'Αδιαφάνεια μπάρας':['Bar opacity','Opacità barra','Opacité de la barre','Leisten-Deckkraft','Непрозрачность панели','信息栏不透明度'],'Χρόνος απόκρυψης':['Auto-hide delay','Ritardo scomparsa','Délai de masquage','Ausblendverzögerung','Время скрытия','自动隐藏延迟']})
    def tr(text):
        if not isinstance(text,str) or language=='GR':return text
        index=('EN','IT','FR','GER','RU','CH').index(language)
        if text in translations:return translations[text][index]
        for key in sorted(translations,key=len,reverse=True):
            if len(key)>=8 and key in text:text=text.replace(key,translations[key][index])
            elif len(key)>=3:text=re.sub(r'(?<!\w)'+re.escape(key)+r'(?!\w)',lambda _:translations[key][index],text)
        return text
    # Preserve original combo keys while displaying translated labels.
    BaseLabel,BaseButton,BaseLine,BaseCombo,BaseMenu,BaseDialog=QLabel,QPushButton,QLineEdit,QComboBox,QMenu,QDialog
    class QLabel(BaseLabel):
        def __init__(self,text='',*args,**kwargs):super().__init__(tr(text),*args,**kwargs);self.original_text=text
        def setText(self,text):self.original_text=text;super().setText(tr(text))
    class QPushButton(BaseButton):
        def __init__(self,text='',*args,**kwargs):super().__init__(tr(text),*args,**kwargs);self.original_text=text
        def setText(self,text):self.original_text=text;super().setText(tr(text))
    class QLineEdit(BaseLine):
        def setPlaceholderText(self,text):self.original_placeholder=text;super().setPlaceholderText(tr(text))
    class QComboBox(BaseCombo):
        def addItem(self,text,userData=None):super().addItem(tr(text),text if userData is None else userData)
        def addItems(self,texts):
            for text in texts:self.addItem(text)
        def currentText(self):return str(self.currentData()) if self.currentData() is not None else super().currentText()
        def setCurrentText(self,text):
            index=self.findData(text)
            if index>=0:self.setCurrentIndex(index)
            else:super().setCurrentText(tr(text))
    class QMenu(BaseMenu):
        def addAction(self,text,*args):return super().addAction(tr(text),*args)
        def addMenu(self,text):
            if isinstance(text,str):menu=QMenu(self);menu.setTitle(tr(text));super().addMenu(menu);return menu
            return super().addMenu(text)
    class QDialog(BaseDialog):
        def setWindowTitle(self,text):super().setWindowTitle(tr(text))
    class QMessageBox(QMessageBox):
        @staticmethod
        def information(parent,title,text):return BaseMessageBox.information(parent,tr(title),tr(text))
        @staticmethod
        def critical(parent,title,text):return BaseMessageBox.critical(parent,tr(title),tr(text))
    # Class reference must be retained separately for static calls above.
    from PySide6.QtWidgets import QMessageBox as BaseMessageBox
    from PySide6.QtWidgets import QInputDialog as BaseInputDialog
    class QInputDialog(BaseInputDialog):
        @staticmethod
        def getText(parent,title,label,*args,**kwargs):return BaseInputDialog.getText(parent,tr(title),tr(label),*args,**kwargs)
    from PySide6.QtWidgets import QFileDialog as BaseFileDialog
    class QFileDialog(BaseFileDialog):
        @staticmethod
        def getOpenFileName(parent,title,*args,**kwargs):return BaseFileDialog.getOpenFileName(parent,tr(title),*args,**kwargs)
        @staticmethod
        def getExistingDirectory(parent,title,*args,**kwargs):return BaseFileDialog.getExistingDirectory(parent,tr(title),*args,**kwargs)

    class Scan(QThread):
        result = Signal(int,int,int,str,str)
        planned = Signal(int,int)
        done = Signal(int)
        def __init__(self,gen,channels,disabled,jobs):
            super().__init__();self.gen=gen;self.channels=list(channels);self.disabled=set(disabled);self.jobs=list(jobs);self.cancel=threading.Event()
        def run(self):
            jobs=list(self.jobs);pool=ThreadPoolExecutor(max_workers=6);pending={};scheduled={(ci,si) for ci,si,_ in jobs};result_states={};total=len(jobs)
            def fill():
                while jobs and not self.cancel.is_set() and len(pending)<6:
                    ci,si,mode=jobs.pop(0);source=self.channels[ci].sources[si]
                    pending[pool.submit(quick_probe if mode=='quick' else probe,source,self.cancel)]=(ci,si)
            try:
                fill()
                while pending and not self.cancel.is_set():
                    ready,_=wait(pending,timeout=.2,return_when=FIRST_COMPLETED)
                    for f in ready:
                        ci,si=pending.pop(f);state,reason=f.result();result_states[(ci,si)]=state
                        self.result.emit(self.gen,ci,si,state,reason)
                        if state=='offline' and not any(result_states.get((ci,i))=='online' for i in range(len(self.channels[ci].sources))):
                            # Check remaining alternatives only when the selected source failed.
                            candidates=[i for i in range(len(self.channels[ci].sources)) if (ci,i) not in scheduled]
                            if candidates:
                                i=candidates[0];scheduled.add((ci,i));jobs.append((ci,i,'quick' if self.channels[ci].sources[i].state=='online' else 'full'));total+=1;self.planned.emit(self.gen,total)
                    fill()
            finally:
                pool.shutdown(wait=True,cancel_futures=True);self.done.emit(self.gen)

    class Loader(QThread):
        loaded=Signal(int,object,str); failed=Signal(int,str)
        def __init__(self,gen,fn,label):super().__init__();self.gen=gen;self.fn=fn;self.label=label
        def run(self):
            try:
                items=self.fn()
                if not items:raise ValueError('Η λίστα δεν περιέχει κανάλια')
                self.loaded.emit(self.gen,items,self.label)
            except Exception as e:
                # Never show URLs, account credentials, or request details.
                self.failed.emit(self.gen,'Δεν φορτώθηκε η λίστα: '+type(e).__name__)

    class Video(QFrame):
        doubleClick=Signal(); activity=Signal()
        def mouseDoubleClickEvent(self,e):self.doubleClick.emit()
        def mouseMoveEvent(self,e):self.activity.emit()

    class Window(QMainWindow):
        def __init__(self):
            super().__init__(); self.setWindowTitle('TVBro • Nick Paridis');self.resize(1380,850);self.setMinimumSize(1100,650)
            self.channels=[];self.current=None;self.source_index=0;self.generation=0;self.load_generation=0;self.workers=[];self.loaders=[]
            self.scan_worker=None;self.scan_done=0;self.recording=False;self.record_path=None;self.rec_started=0;self.play_started=0;self.tried=set();self.closing=False;self.full=False;self.auto_hide=bool(settings.get('auto_hide',True));self.rec_format=settings.get('record_format','Auto');self.rec_wait_failed=False;self.overlay_opacity=max(10,min(100,int(settings.get('overlay_opacity',72))));self.hide_delay=max(1,min(3600,int(settings.get('hide_delay',4))));self.theme=settings.get('theme','Auto');self.sidebar_open=True;self.hud_visible=True;self.last_activity=time.monotonic();self.last_cursor=QCursor.pos();self.scan_total=0;self.scan_mode='';self.status_history={}
            try:self.status_history=json.loads(catalog_file.read_text(encoding='utf-8')).get('sources',{})
            except Exception:pass
            self.player=engine.media_player_new() if engine else None
            self.rec_folder=Path(settings.get('record_folder',str(Path.home()/'Videos/GreekTV Recordings')))
            self.favorites=set(settings.get('favorites',[]));self.only_fav=False
            self.favorite_groups=settings.get('favorite_groups',{});self.hidden=set(settings.get('hidden',[]));self.disabled=set(settings.get('disabled',[]));self.saved_order=settings.get('order',[]);self.show_sources=bool(settings.get('show_sources',False))
            self.build();self.apply_theme();self.apply_language(language);app.styleHints().colorSchemeChanged.connect(lambda *_:self.apply_theme() if self.theme=='Auto' else None);app.installEventFilter(self);self.hud_timer=QTimer(self);self.hud_timer.timeout.connect(self.check_hud);self.hud_timer.start(150);self.catalog_timer=QTimer(self);self.catalog_timer.setSingleShot(True);self.catalog_timer.timeout.connect(self.save_catalog);self.timer=QTimer(self);self.timer.timeout.connect(self.tick);self.timer.start(500)
            for seq,fn in [('Space',self.pause),('F',self.fullscreen),('Escape',self.exit_fullscreen),('L',self.go_live),('R',self.record),('M',self.mute),('Ctrl+O',self.open_file),('Ctrl+I',self.info),('Ctrl+B',self.toggle_sidebar),('I',self.show_hud),('Up',lambda:self.navigate(-1)),('Down',lambda:self.navigate(1))]:
                QShortcut(QKeySequence(seq),self,activated=fn)
            QTimer.singleShot(100,self.load_default)
        def button(self,text,fn,obj=''):
            b=QPushButton(text);b.clicked.connect(fn)
            if obj:b.setObjectName(obj)
            return b
        def build(self):
            central=QWidget();self.setCentralWidget(central);outer=QVBoxLayout(central);self.outer_layout=outer;outer.setContentsMargins(12,10,12,10);outer.setSpacing(8)
            header=QHBoxLayout();self.menu_button=self.button('☰',self.toggle_sidebar,'ghost');self.menu_button.setToolTip('Κανάλια • Ctrl+B');self.menu_button.setFixedWidth(48);header.addWidget(self.menu_button)
            title=QLabel('TVBro  /  LIVE TV');title.setObjectName('brand');header.addWidget(title);header.addStretch()
            self.summary=QLabel('Έλεγχος καναλιών');self.summary.setObjectName('muted');self.summary.setMinimumWidth(235);header.addWidget(self.summary)
            self.gear_top=self.icon_button('gear',self.settings_dialog,'Ρυθμίσεις');header.addWidget(self.gear_top);header.addWidget(self.icon_button('info',self.info,'Info'));self.header_widget=QWidget();self.header_widget.setLayout(header);outer.addWidget(self.header_widget)
            self.splitter=QSplitter();outer.addWidget(self.splitter,1)
            self.sidebar=QFrame();self.sidebar.setObjectName('panel');side=QVBoxLayout(self.sidebar);side.setContentsMargins(10,10,10,10);side.setSpacing(7)
            self.source_label=QLabel('Greek TV • ενσωματωμένη λίστα');self.source_label.setWordWrap(True);side.addWidget(self.source_label)
            self.search=QLineEdit();self.search.setPlaceholderText('Αναζήτηση καναλιού…');self.search.textChanged.connect(self.refresh);side.addWidget(self.search)
            self.category=QComboBox();self.category.addItem('Όλες οι κατηγορίες');self.category.currentIndexChanged.connect(self.refresh);side.addWidget(self.category)
            self.fav_filter=QComboBox();self.fav_filter.addItems(['Όλα τα κανάλια','★ Αγαπημένα']+list(self.favorite_groups));self.fav_filter.currentIndexChanged.connect(self.refresh);side.addWidget(self.fav_filter)
            self.list=QListWidget();self.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu);self.list.customContextMenuRequested.connect(self.channel_menu);self.list.itemDoubleClicked.connect(self.list_play);self.list.itemActivated.connect(self.list_play);side.addWidget(self.list,1)
            orderrow=QHBoxLayout();orderrow.addWidget(self.button('↑ Move',lambda:self.move_channel(-1)));orderrow.addWidget(self.button('↓ Move',lambda:self.move_channel(1)));side.addLayout(orderrow)
            self.progress=QProgressBar();side.addWidget(self.progress)
            row=QHBoxLayout();row.addWidget(self.button('↻ Quick',lambda:self.scan(False)));row.addWidget(self.button('Διακοπή',self.cancel_scan));side.addLayout(row)
            self.count_label=QLabel('Εμφάνιση μόνο διαθέσιμων καναλιών');self.count_label.setObjectName('muted');self.count_label.setWordWrap(True);side.addWidget(self.count_label)
            footer=QHBoxLayout();footer.setSpacing(8);footer.addStretch();footer.addWidget(self.icon_button('gear',self.settings_dialog,'Ρυθμίσεις'));footer.addWidget(self.icon_button('info',self.info,'Info'));footer.addWidget(self.icon_button('about',self.about,'About'));footer.addStretch();side.addLayout(footer)
            self.splitter.addWidget(self.sidebar)
            right=QWidget();rv=QVBoxLayout(right);self.video_layout=rv;rv.setContentsMargins(0,0,0,0);rv.setSpacing(10)
            self.video=Video();self.video.setStyleSheet('background:#000000;border-radius:10px;');self.video.setAttribute(Qt.WidgetAttribute.WA_NativeWindow);self.video.setMouseTracking(True);self.video.doubleClick.connect(self.fullscreen);self.video.activity.connect(self.show_hud)
            vl=QVBoxLayout(self.video);vl.addStretch();self.video_placeholder=QLabel('TVBro\n\nΔιπλό κλικ σε διαθέσιμο κανάλι για αναπαραγωγή');self.video_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter);self.video_placeholder.setStyleSheet('color:#617992;font-size:20px;background:transparent;');vl.addWidget(self.video_placeholder);vl.addStretch();rv.addWidget(self.video,1)
            self.infobar=QFrame();self.infobar.setObjectName('panel');ib=QHBoxLayout(self.infobar)
            self.channel_number=QLabel('—');self.channel_number.setMinimumWidth(64);self.channel_number.setStyleSheet('font-size:28px;color:#5ee0da;font-weight:700;');ib.addWidget(self.channel_number)
            names=QVBoxLayout();self.channel_title=QLabel('Διάλεξε κανάλι');self.channel_title.setStyleSheet('font-size:19px;font-weight:700;');names.addWidget(self.channel_title)
            self.stream_label=QLabel('LIVE • Έλεγχος πηγών στο παρασκήνιο');self.stream_label.setObjectName('muted');names.addWidget(self.stream_label);ib.addLayout(names,1)
            self.clock=QLabel();self.clock.setStyleSheet('font-size:18px;');ib.addWidget(self.clock);self.fav_button=self.button('☆',self.favorite);ib.addWidget(self.fav_button);rv.addWidget(self.infobar)
            self.controls=QFrame();self.controls.setObjectName('panel');cv=QVBoxLayout(self.controls)
            seekrow=QHBoxLayout();self.elapsed=QLabel('00:00');seekrow.addWidget(self.elapsed);self.seek=QSlider(Qt.Orientation.Horizontal);self.seek.setRange(0,1000);self.seek.sliderReleased.connect(self.seek_release);seekrow.addWidget(self.seek,1);self.duration=QLabel('LIVE');seekrow.addWidget(self.duration);cv.addLayout(seekrow)
            row=QHBoxLayout();row.addWidget(self.button('◀|' ,lambda:self.navigate(-1)));self.pause_button=self.button('Ⅱ Pause',self.pause);row.addWidget(self.pause_button);row.addWidget(self.button('■',self.stop));row.addWidget(self.button('|▶',lambda:self.navigate(1)))
            row.addWidget(self.button('● Go Live',self.go_live,'primary'));self.rec_button=self.button('● REC',self.record,'record');self.rec_button.setCheckable(True);row.addWidget(self.rec_button)
            row.addWidget(self.button('⋯',self.playback_menu));row.addWidget(self.icon_button('full',self.fullscreen,'Fullscreen / F'));self.full_gear=self.icon_button('gear',self.settings_dialog,'Ρυθμίσεις');row.addWidget(self.full_gear);row.addStretch();self.mute_button=self.button('Vol',self.mute);row.addWidget(self.mute_button)
            self.volume=QSlider(Qt.Orientation.Horizontal);self.volume.setRange(0,100);self.volume.setValue(int(settings.get('volume',80)));self.volume.setMaximumWidth(110);self.volume.valueChanged.connect(self.set_volume);row.addWidget(self.volume);self.volume_label=QLabel(str(self.volume.value())+'%');row.addWidget(self.volume_label);cv.addLayout(row);rv.addWidget(self.controls)
            self.splitter.addWidget(right);self.splitter.setSizes([290,940]);self.splitter.setStretchFactor(1,1)
            self.notice=QLabel('Έτοιμο');self.notice.setObjectName('muted');self.notice.setWordWrap(True);outer.addWidget(self.notice)
            self.overlay=QWidget(self,Qt.WindowType.Tool|Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowDoesNotAcceptFocus);self.overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground);self.overlay.setObjectName('videoHUD');self.overlay_layout=QVBoxLayout(self.overlay);self.overlay_layout.setContentsMargins(0,0,0,0);self.overlay_layout.setSpacing(6);rv.removeWidget(self.infobar);self.infobar.setParent(self.overlay);self.overlay_layout.addWidget(self.infobar);self.overlay.hide();self.apply_overlay_style()
            if self.player:
                handle=int(self.video.winId())
                if os.name=='nt':self.player.set_hwnd(handle)
                elif sys.platform=='darwin':self.player.set_nsobject(handle)
                else:self.player.set_xwindow(handle)
                self.player.video_set_mouse_input(False);self.player.video_set_key_input(False)
        def menu(self):
            m=QMenu(self);m.setWindowOpacity(.94)
            for label,fn in [('Ενσωματωμένη Greek TV',self.load_default),('Άνοιγμα M3U / M3U8…',self.open_file),('M3U από URL…',self.open_url),('Xtream Codes…',self.open_xtream),('Όλες οι πηγές: '+('ON' if self.show_sources else 'OFF'),self.toggle_sources),('Διαχείριση ομάδων αγαπημένων',self.manage_groups),('Κρυφά / Disabled κανάλια',self.manage_hidden),('Εμφάνιση αγαπημένων',self.toggle_favorites),('Φάκελος εγγραφών…',self.choose_record_folder),('Άνοιγμα εγγραφών',lambda:QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.rec_folder)))),('Γρήγορος έλεγχος αλλαγών',lambda:self.scan(False)),('Πλήρης έλεγχος όλων',lambda:self.scan(True)),('Auto-hide: '+('ON' if self.auto_hide else 'OFF'),self.toggle_auto_hide),('Info / κατάσταση καναλιών',self.info),('Οδηγίες / About',self.about)]:m.addAction(label,fn)
            anchor=self.full_gear if self.full else self.gear_top;m.exec(anchor.mapToGlobal(anchor.rect().bottomLeft()))
        def icon_button(self,kind,callback,tooltip):
            button=self.button('',callback,'ghost');button.setToolTip(tr(tooltip));button.setFixedSize(36,34)
            pixmap=QPixmap(40,40);pixmap.fill(Qt.GlobalColor.transparent);painter=QPainter(pixmap);painter.setRenderHint(QPainter.RenderHint.Antialiasing);painter.setPen(QColor('#56b7ba'))
            if kind=='full':
                for x,y,dx,dy in [(8,8,1,1),(32,8,-1,1),(8,32,1,-1),(32,32,-1,-1)]:painter.drawLine(x,y,x+dx*8,y);painter.drawLine(x,y,x,y+dy*8)
            elif kind=='gear':
                painter.setBrush(QColor('#56b7ba'));painter.translate(20,20)
                for _ in range(10):painter.drawRect(-3,-17,6,7);painter.rotate(36)
                painter.drawEllipse(-12,-12,24,24);painter.setBrush(QColor('#132036'));painter.drawEllipse(-5,-5,10,10)
            else:
                painter.setFont(QFont('Segoe UI',21,QFont.Weight.Bold));painter.drawText(pixmap.rect(),Qt.AlignmentFlag.AlignCenter,'i' if kind=='info' else '?')
            painter.end();button.setIcon(QIcon(pixmap));return button
        def apply_theme(self):
            light=self.theme=='Light' or (self.theme=='Auto' and app.styleHints().colorScheme()==Qt.ColorScheme.Light)
            app.setStyleSheet(light_style if light else dark_style)
            if hasattr(self,'overlay'):self.apply_overlay_style()
        def apply_language(self,code):
            nonlocal language
            language=code
            app.removeTranslator(qt_translator)
            locale={'EN':'en','GR':'el','IT':'it','FR':'fr','GER':'de','RU':'ru','CH':'zh_CN'}[code]
            if qt_translator.load('qtbase_'+locale,QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):app.installTranslator(qt_translator)
            for widget in self.findChildren(BaseLabel)+self.findChildren(BaseButton):
                if hasattr(widget,'original_text'):widget.setText(widget.original_text)
            for widget in self.findChildren(BaseLine):
                if hasattr(widget,'original_placeholder'):widget.setPlaceholderText(widget.original_placeholder)
            for combo in self.findChildren(BaseCombo):
                combo.blockSignals(True)
                for i in range(combo.count()):combo.setItemText(i,tr(str(combo.itemData(i))))
                combo.blockSignals(False)
            self.refresh();self.save_preferences()
        def settings_dialog(self):
            self.show_hud();d=QDialog(self);d.setWindowTitle('Ρυθμίσεις');d.resize(500,480);layout=QVBoxLayout(d);form=QFormLayout();theme=QComboBox();theme.addItems(['Dark','Light','Auto']);theme.setCurrentText(self.theme)
            langs=QComboBox()
            for code,label in [('EN','English'),('GR','Ελληνικά'),('IT','Italiano'),('FR','Français'),('GER','Deutsch'),('RU','Русский'),('CH','中文')]:langs.addItem(label,code)
            langs.setCurrentText(language);form.addRow(tr('Θέμα εμφάνισης'),theme);form.addRow(tr('Γλώσσα'),langs);recformat=QComboBox();recformat.addItems(['Auto','MKV','TS']);recformat.setCurrentText(self.rec_format);form.addRow('REC format',recformat);recformat.currentIndexChanged.connect(lambda:(setattr(self,'rec_format',recformat.currentText()),self.save_preferences()));layout.addLayout(form)
            def change_theme():self.theme=theme.currentText();self.apply_theme();self.save_preferences()
            theme.currentIndexChanged.connect(change_theme);langs.currentIndexChanged.connect(lambda:self.apply_language(langs.currentData()))
            opacity=QSlider(Qt.Orientation.Horizontal);opacity.setRange(10,100);opacity.setValue(self.overlay_opacity);opacity_label=QLabel(f'{self.overlay_opacity}%');opacity_row=QHBoxLayout();opacity_row.addWidget(opacity);opacity_row.addWidget(opacity_label);form.addRow(tr('Αδιαφάνεια μπάρας'),opacity_row)
            delay=QSpinBox();delay.setRange(1,3600);delay.setSuffix(' s');delay.setValue(self.hide_delay);delay_label=QLabel(f'{self.hide_delay}s');delay_row=QHBoxLayout();delay_row.addWidget(delay);delay_row.addWidget(delay_label);form.addRow(tr('Χρόνος απόκρυψης'),delay_row)
            def change_opacity(value):self.overlay_opacity=value;opacity_label.setText(f'{value}%');self.apply_overlay_style();self.save_preferences()
            def change_delay(value):self.hide_delay=value;delay_label.setText(f'{value}s');self.save_preferences()
            opacity.valueChanged.connect(change_opacity);delay.valueChanged.connect(change_delay)
            autohide=QCheckBox(tr('Αυτόματη απόκρυψη'));autohide.setChecked(self.auto_hide);form.addRow(autohide);autohide.toggled.connect(lambda value:(setattr(self,'auto_hide',value),self.show_hud(),self.save_preferences()))
            for label,callback in [('Ενσωματωμένη Greek TV',self.load_default),('Άνοιγμα M3U / M3U8…',self.open_file),('M3U από URL…',self.open_url),('Xtream Codes…',self.open_xtream),('Διαχείριση ομάδων αγαπημένων',self.manage_groups),('Κρυφά / Disabled κανάλια',self.manage_hidden),('Φάκελος εγγραφών…',self.choose_record_folder)]:
                layout.addWidget(self.button(label,lambda checked=False,fn=callback:(d.accept(),fn())))
            layout.addWidget(self.button('Περισσότερες ρυθμίσεις…',lambda:(d.accept(),self.menu())))
            layout.addWidget(self.button('Κλείσιμο',d.accept));d.exec()
        def load_default(self):
            self.request_load(lambda:parse_m3u(zlib.decompress(base64.b64decode(DEFAULT_PLAYLIST)).decode('utf-8')),'Greek TV • ενσωματωμένη λίστα')
        def request_load(self,fn,label):
            self.load_generation+=1;w=Loader(self.load_generation,fn,label);self.loaders.append(w);w.loaded.connect(self.loaded);w.failed.connect(self.load_error)
            w.finished.connect(lambda:self.cleanup_loader(w));self.notice.setText('Φόρτωση λίστας…');w.start()
        def cleanup_loader(self,w):
            if w in self.loaders:self.loaders.remove(w)
            w.deleteLater()
        def load_error(self,gen,error):
            if gen==self.load_generation:self.notice.setText(error)
        def loaded(self,gen,items,label):
            if gen!=self.load_generation:return
            self.stop();self.cancel_scan();self.channels=items;self.current=None
            positions={key:i for i,key in enumerate(self.saved_order)};self.channels.sort(key=lambda c:positions.get(c.key,len(positions)));self.source_label.setText(label);self.only_fav=False
            self.category.blockSignals(True);self.category.clear();self.category.addItem('Όλες οι κατηγορίες');self.category.addItems(sorted({c.group for c in items}));self.category.blockSignals(False)
            self.restore_catalog()
            if demo:self.refresh()
            else:self.scan(False)
        def open_file(self):
            path,_=QFileDialog.getOpenFileName(self,'Φόρτωση λίστας','','Playlists (*.m3u *.m3u8);;All files (*)')
            if path:self.request_load(lambda:parse_m3u(Path(path).read_text(encoding='utf-8-sig',errors='replace')),Path(path).name)
        def open_url(self):
            url,ok=QInputDialog.getText(self,'M3U URL','URL λίστας (HTTP/HTTPS):')
            if ok and url.strip():self.request_load(lambda:parse_m3u(fetch(url.strip(),limit=24_000_000,timeout=20)[0].decode('utf-8-sig','replace')),'M3U • URL')
        def open_xtream(self):
            d=QDialog(self);d.setWindowTitle('Xtream Codes • Live TV');form=QFormLayout(d);server=QLineEdit();server.setPlaceholderText('https://server:port');user=QLineEdit();pwd=QLineEdit();pwd.setEchoMode(QLineEdit.EchoMode.Password)
            form.addRow('Server',server);form.addRow('Username',user);form.addRow('Password',pwd);note=QLabel('Τα στοιχεία σύνδεσης διατηρούνται μόνο στη μνήμη.\nΟ έλεγχος χρησιμοποιεί έως 6 παράλληλα HTTP requests.');form.addRow(note)
            buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel);buttons.accepted.connect(d.accept);buttons.rejected.connect(d.reject);form.addRow(buttons)
            if d.exec():
                s,u,p=server.text().strip(),user.text().strip(),pwd.text();self.request_load(lambda:xtream_channels(s,u,p),'Xtream Codes • Live TV')
        def cancel_scan(self):
            if self.scan_worker and self.scan_worker.isRunning():self.scan_worker.cancel.set()
            self.generation+=1;self.scan_worker=None
        def restore_catalog(self):
            now=time.time()
            for ch in self.channels:
                for source in ch.sources:
                    record=self.status_history.get(source_key(source),{})
                    timestamp=record.get('checked_at',0)
                    if record.get('state') in ('online','offline') and isinstance(timestamp,(float,int)) and 0<=now-timestamp<30*86400:
                        source.state=record['state'];source.reason='Αποθηκευμένος έλεγχος • '+record.get('reason','');source.metadata=record.get('metadata',{});source.checked_at=timestamp
            self.refresh()
        def save_catalog(self):
            if demo:return
            now=time.time()
            for ch in self.channels:
                for source in ch.sources:
                    if source.state in ('online','offline') and source.checked_at and ch.key not in self.disabled:
                        self.status_history[source_key(source)]={'state':source.state,'reason':source.reason.replace('Αποθηκευμένος έλεγχος • ',''),'metadata':source.metadata,'checked_at':source.checked_at}
            self.status_history={k:v for k,v in self.status_history.items() if 0<=now-v.get('checked_at',0)<30*86400}
            try:
                temp=catalog_file.with_suffix('.tmp');temp.write_text(json.dumps({'schema':1,'sources':self.status_history},ensure_ascii=False),encoding='utf-8');temp.replace(catalog_file)
            except OSError:self.notice.setText('Δεν αποθηκεύτηκαν οι καταστάσεις καναλιών.')
        def scan(self,full=False):
            self.cancel_scan();self.scan_done=0
            if full:
                jobs=[(ci,si,'full') for ci,c in enumerate(self.channels) if c.key not in self.disabled for si,_ in enumerate(c.sources)]
                self.scan_mode='Πλήρης έλεγχος'
            else:
                jobs=check_plan(self.channels,self.disabled);self.scan_mode='Πρώτος έλεγχος' if jobs and all(mode=='full' for _,_,mode in jobs) and not any(s.checked_at for c in self.channels for s in c.sources) else 'Γρήγορος έλεγχος αλλαγών'
            self.scan_total=len(jobs)
            if not jobs:
                self.notice.setText('Αποθηκευμένη λίστα έτοιμη • δεν υπάρχουν νέες πηγές ή έλεγχοι σε αναμονή.');self.refresh();return
            gen=self.generation;w=Scan(gen,self.channels,self.disabled,jobs);self.scan_worker=w;self.workers.append(w);w.result.connect(self.scan_result);w.planned.connect(self.scan_planned);w.done.connect(self.scan_finished);w.finished.connect(lambda:self.cleanup_worker(w));w.start();self.refresh();self.notice.setText(f'{self.scan_mode} • {len(jobs)} πηγές, με εμφάνιση της αποθηκευμένης λίστας.')
        def scan_planned(self,gen,total):
            if gen==self.generation:self.scan_total=total;self.refresh()
        def cleanup_worker(self,w):
            if w in self.workers:self.workers.remove(w)
            w.deleteLater()
        def scan_result(self,gen,ci,si,state,reason):
            if gen!=self.generation:return
            s=self.channels[ci].sources[si];s.state='offline' if self.channels[ci].key in self.disabled else state;s.reason='Disabled' if self.channels[ci].key in self.disabled else reason;s.checked_at=time.time();self.scan_done+=1;self.refresh()
            if not self.catalog_timer.isActive():self.catalog_timer.start(800)
        def scan_finished(self,gen):
            if gen!=self.generation:return
            self.scan_worker=None;self.save_catalog();self.notice.setText(f'{self.scan_mode} ολοκληρώθηκε • {self.scan_done} πηγές ελέγχθηκαν. Οι υπόλοιπες κρατούν την τελευταία κατάσταση.');self.refresh()
        def refresh(self,*args):
            selected=self.list.currentItem();old=selected.data(Qt.ItemDataRole.UserRole) if selected else None
            self.list.clear();query=self.search.text().casefold();cat=self.category.currentText();fav_group=self.fav_filter.currentText()
            for i,c in enumerate(self.channels):
                if c.key in self.hidden or c.key in self.disabled or (fav_group=='★ Αγαπημένα' and c.key not in self.favorites) or (fav_group in self.favorite_groups and c.key not in self.favorite_groups[fav_group]) or c.state!='online' or query not in c.name.casefold() or (cat!='Όλες οι κατηγορίες' and c.group!=cat) or (self.only_fav and c.key not in self.favorites):continue
                candidates=[n for n,source in enumerate(c.sources) if source.state=='online']
                for source_index in (candidates if self.show_sources else candidates[:1]):
                    suffix=f' • Πηγή {source_index+1}' if self.show_sources else ''
                    item=QListWidgetItem(('★ ' if c.key in self.favorites else '')+f'{i+1:03d}  {c.name}{suffix}\n       ● LIVE  ·  {c.group}')
                    item.setData(Qt.ItemDataRole.UserRole,(i,source_index));self.list.addItem(item)
                    if old==(i,source_index):self.list.setCurrentItem(item)
            online=sum(c.state=='online' for c in self.channels);offline=sum(c.state=='offline' for c in self.channels);pending=len(self.channels)-online-offline
            self.summary_text=f'Total {len(self.channels)}  •  On Air {online}  •  Offline {offline}  •  Pending {pending}';self.summary.setText(f'{len(self.channels)} κανάλια  •  {online} On Air');self.summary.setToolTip(self.summary_text)
            self.progress.setRange(0,max(self.scan_total,1));self.progress.setValue(self.scan_done if self.scan_total else 1);self.progress.setFormat(f'{self.scan_done}/{self.scan_total} πηγές  ·  %p%' if self.scan_total else 'Έτοιμο')
            self.count_label.setText(f'{self.list.count()} διαθέσιμα στη λίστα'+(' • Αγαπημένα' if self.only_fav else ''))
        def list_play(self,item):
            index,source=item.data(Qt.ItemDataRole.UserRole);self.tried=set();self.search.clearFocus();self.video.setFocus();self.play_channel(index,source)
        def play_channel(self,index,source=None,record_path=None):
            if not self.player:self.notice.setText('Demo UI • χωρίς VLC playback');return
            if self.recording:self.finish_recording(restart=False)
            channel=self.channels[index]
            if channel.key in self.disabled:return
            if source is None:
                self.tried=set();source=next((i for i,s in enumerate(channel.sources) if s.state=='online'),0)
            self.current=index;self.source_index=source;self.tried.add(source);self.video_placeholder.hide();self.show_hud()
            self.player.stop();s=channel.sources[source];media=engine.media_new(s.url);media.add_option(':network-caching=1200');media.add_option(':input-timeshift-path='+str(temp_root))
            for k,v in s.headers.items():
                k=k.lower()
                if '\r' in v or '\n' in v:continue
                if k=='referer':media.add_option(':http-referrer='+v)
                elif k=='user-agent':media.add_option(':http-user-agent='+v)
                elif k in ('origin','cookie','authorization'):media.add_option(':http-header='+k+'='+v)
            if record_path:
                # VLC 3.x has no stable public toggle-record API: restart with stream-output.
                dst=record_path.as_posix().replace("'",'');mux='avformat{mux=matroska}' if record_path.suffix=='.mkv' else 'ts'
                media.add_option(":sout=#duplicate{dst=display,dst=std{access=file,mux="+mux+",dst='"+dst+"'}}")
                media.add_option(':sout-all');media.add_option(':sout-mux-caching=1000')
            self.player.set_media(media);media.release();self.player.audio_set_volume(self.volume.value());result=self.player.play();self.play_started=time.monotonic()
            self.channel_number.setText(f'{index+1:03d}');self.channel_title.setText(channel.name);self.fav_button.setText('★' if channel.key in self.favorites else '☆');self.pause_button.setText('Ⅱ Pause')
            self.notice.setText('Σύνδεση…' if result==0 else 'Το VLC δεν μπόρεσε να ξεκινήσει τη ροή')
        def navigate(self,delta):
            ids=list(dict.fromkeys(self.list.item(i).data(Qt.ItemDataRole.UserRole)[0] for i in range(self.list.count())))
            if not ids:return
            pos=ids.index(self.current) if self.current in ids else (-1 if delta>0 else 0);self.play_channel(ids[(pos+delta)%len(ids)])
        def pause(self):
            if not self.player or self.current is None:return
            if not self.player.can_pause():self.notice.setText('Αυτή η ζωντανή ροή δεν υποστηρίζει pause / timeshift.');return
            self.player.pause()
        def stop(self):
            if self.recording:self.finish_recording(restart=False)
            if self.player:self.player.stop()
            self.play_started=0;self.show_hud();self.video_placeholder.show();self.notice.setText('Αναπαραγωγή σταματημένη')
        def go_live(self):
            if self.current is not None:
                was_recording=self.recording;self.play_channel(self.current,self.source_index);self.notice.setText('Επανασύνδεση στη ζωντανή ροή'+(' • Η εγγραφή αποθηκεύτηκε και σταμάτησε' if was_recording else ''))
        def set_volume(self,value):
            self.volume_label.setText(f'{value}%')
            if self.player:self.player.audio_set_volume(value)
        def mute(self):
            if self.player:self.player.audio_toggle_mute();self.mute_button.setText('Mute' if self.player.audio_get_mute() else 'Vol')
        def seek_release(self):
            if self.player and self.player.is_seekable():self.player.set_position(self.seek.value()/1000)
        def choose_record_folder(self):
            folder=QFileDialog.getExistingDirectory(self,'Φάκελος εγγραφών',str(self.rec_folder))
            if folder:self.rec_folder=Path(folder);self.save_preferences()
        def record(self):
            if self.recording:self.finish_recording();return
            if self.current is None or not self.player:self.rec_button.setChecked(False);return
            try:
                self.rec_folder.mkdir(parents=True,exist_ok=True)
                name=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',self.channels[self.current].name).replace("'",'_').strip(' .')[:70] or 'Channel'
                source=self.channels[self.current].sources[self.source_index];codecs=[]
                try:
                    for track in self.player.get_media().tracks_get() or []:codecs.append(int(track.codec).to_bytes(4,'little').decode('ascii','ignore').lower())
                except Exception:pass
                extension,_=recording_format(source,self.rec_format,codecs)
                path=self.rec_folder/(name+'_'+time.strftime('%Y%m%d_%H%M%S')+'_'+str(time.time_ns()%1000000)+extension)
                # Verify directory access without pre-creating the output VLC must create.
                with tempfile.TemporaryFile(dir=self.rec_folder) as testfile:testfile.write(b'test')
                self.play_channel(self.current,self.source_index,record_path=path);self.recording=True;self.record_path=path;self.rec_wait_failed=False;self.rec_started=time.monotonic();self.rec_button.setChecked(True);self.notice.setText('VLC REC • Η ροή επανασυνδέθηκε για να ξεκινήσει η εγγραφή.')
            except Exception:
                self.rec_button.setChecked(False);self.notice.setText('Δεν μπορεί να ξεκινήσει η εγγραφή στον επιλεγμένο φάκελο.')
        def finish_recording(self,restart=True):
            path=self.record_path;self.recording=False;self.rec_button.setChecked(False);self.rec_button.setText('● REC')
            if self.player:self.player.stop()
            self.record_path=None
            if restart and self.current is not None:self.play_channel(self.current,self.source_index)
            if path:
                try:size=path.stat().st_size
                except OSError:size=0
                valid=recording_valid(path);self.notice.setText(f'Εγγραφή: {path.name} • {size/1048576:.1f} MB' if valid else 'REC απέτυχε: κενό ή μη αναγνωρίσιμο αρχείο. Δοκίμασε MKV από τις ρυθμίσεις.');
                if not valid:QMessageBox.information(self,'REC','REC απέτυχε: κενό ή μη αναγνωρίσιμο αρχείο. Δοκίμασε MKV από τις ρυθμίσεις.')
        def favorite(self):
            if self.current is None:return
            key=self.channels[self.current].key
            if key in self.favorites:self.favorites.remove(key)
            else:self.favorites.add(key)
            self.fav_button.setText('★' if key in self.favorites else '☆');self.refresh();self.save_preferences()
        def toggle_favorites(self):self.only_fav=not self.only_fav;self.refresh()
        def save_preferences(self):
            if self.channels:self.saved_order=[c.key for c in self.channels]
            data={'volume':self.volume.value(),'record_folder':str(self.rec_folder),'favorites':list(self.favorites),'favorite_groups':self.favorite_groups,'hidden':list(self.hidden),'disabled':list(self.disabled),'order':self.saved_order,'show_sources':self.show_sources,'auto_hide':self.auto_hide,'theme':self.theme,'language':language,'overlay_opacity':self.overlay_opacity,'hide_delay':self.hide_delay,'record_format':self.rec_format}
            try:
                tmp=config_file.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');tmp.replace(config_file)
            except OSError:self.notice.setText('Δεν αποθηκεύτηκαν οι προτιμήσεις.')
        def toggle_sources(self):self.show_sources=not self.show_sources;self.refresh();self.save_preferences()
        def selected_index(self):
            item=self.list.currentItem()
            return item.data(Qt.ItemDataRole.UserRole)[0] if item else None
        def move_channel(self,delta):
            index=self.selected_index()
            if index is None:return
            visible=list(dict.fromkeys(self.list.item(i).data(Qt.ItemDataRole.UserRole)[0] for i in range(self.list.count())))
            pos=visible.index(index);otherpos=pos+delta
            if not 0<=otherpos<len(visible):return
            other=visible[otherpos];current_key=self.channels[self.current].key if self.current is not None else None
            # Cancel an active scan before reordering indexed results.
            was_scanning=self.scan_worker is not None
            self.cancel_scan();self.channels[index],self.channels[other]=self.channels[other],self.channels[index]
            if current_key:self.current=next(i for i,c in enumerate(self.channels) if c.key==current_key)
            self.refresh();self.save_preferences()
            for i in range(self.list.count()):
                if self.list.item(i).data(Qt.ItemDataRole.UserRole)[0]==other:self.list.setCurrentRow(i);break
            if was_scanning:self.notice.setText('Η σειρά αποθηκεύτηκε. Πάτησε Quick για να συνεχίσει ο έλεγχος.')
        def channel_menu(self,position):
            item=self.list.itemAt(position)
            if not item:return
            self.list.setCurrentItem(item);idx=item.data(Qt.ItemDataRole.UserRole)[0];ch=self.channels[idx];m=QMenu(self)
            m.addAction('Αναπαραγωγή',lambda:self.list_play(item))
            m.addAction('↑ Μετακίνηση πάνω',lambda:self.move_channel(-1));m.addAction('↓ Μετακίνηση κάτω',lambda:self.move_channel(1))
            m.addAction('★ Αγαπημένο',lambda:self.toggle_channel_favorite(ch))
            groups=m.addMenu('Ομάδες αγαπημένων')
            for name in self.favorite_groups:
                a=groups.addAction(name);a.setCheckable(True);a.setChecked(ch.key in self.favorite_groups[name]);a.triggered.connect(lambda checked,n=name:self.assign_group(ch,n,checked))
            groups.addAction('Νέα ομάδα…',lambda:self.new_group(ch))
            m.addAction('Hide — απόκρυψη',lambda:self.flag_channel(ch,'hidden'));m.addAction('Disable — απενεργοποίηση',lambda:self.flag_channel(ch,'disabled'))
            m.exec(self.list.mapToGlobal(position))
        def toggle_channel_favorite(self,ch):
            if ch.key in self.favorites:self.favorites.remove(ch.key)
            else:self.favorites.add(ch.key)
            self.refresh();self.save_preferences()
        def assign_group(self,ch,name,checked=True):
            values=set(self.favorite_groups.get(name,[]))
            if checked:values.add(ch.key)
            else:values.discard(ch.key)
            self.favorite_groups[name]=list(values);self.refresh();self.save_preferences()
        def new_group(self,ch=None):
            name,ok=QInputDialog.getText(self,'Νέα ομάδα αγαπημένων','Όνομα ομάδας:')
            name=name.strip()
            if ok and name and name not in ('Όλα τα κανάλια','★ Αγαπημένα'):
                self.favorite_groups.setdefault(name,[])
                if ch:self.assign_group(ch,name)
                self.update_group_filter();self.save_preferences()
        def update_group_filter(self):
            old=self.fav_filter.currentText();self.fav_filter.blockSignals(True);self.fav_filter.clear();self.fav_filter.addItems(['Όλα τα κανάλια','★ Αγαπημένα']+list(self.favorite_groups));self.fav_filter.setCurrentText(old);self.fav_filter.blockSignals(False);self.refresh()
        def manage_groups(self):
            d=QDialog(self);d.setWindowTitle('Ομάδες αγαπημένων');layout=QVBoxLayout(d);lst=QListWidget();layout.addWidget(lst)
            def refill():lst.clear();lst.addItems(list(self.favorite_groups))
            def add():self.new_group();refill()
            def rename():
                item=lst.currentItem()
                if not item:return
                old=item.text();name,ok=QInputDialog.getText(d,'Μετονομασία','Νέο όνομα:',text=old);name=name.strip()
                if ok and name and name not in self.favorite_groups and name not in ('Όλα τα κανάλια','★ Αγαπημένα'):
                    self.favorite_groups[name]=self.favorite_groups.pop(old);self.update_group_filter();self.save_preferences();refill()
            row=QHBoxLayout();row.addWidget(self.button('Νέα ομάδα',add));row.addWidget(self.button('Μετονομασία',rename));layout.addLayout(row);layout.addWidget(QLabel('Δεξί κλικ σε κανάλι → Ομάδες αγαπημένων.'));refill();d.exec()
        def flag_channel(self,ch,kind):
            getattr(self,kind).add(ch.key)
            if kind=='disabled' and self.current is not None and self.channels[self.current].key==ch.key:self.stop()
            self.refresh();self.save_preferences()
        def manage_hidden(self):
            d=QDialog(self);d.setWindowTitle('Κρυφά / Disabled — επαναφορά');d.resize(560,380);layout=QVBoxLayout(d);lst=QListWidget();layout.addWidget(lst)
            def refill():
                lst.clear()
                for ch in self.channels:
                    if ch.key in self.hidden or ch.key in self.disabled:
                        item=QListWidgetItem(ch.name+' • '+('Hidden ' if ch.key in self.hidden else '')+('Disabled' if ch.key in self.disabled else ''));item.setData(Qt.ItemDataRole.UserRole,ch.key);lst.addItem(item)
            def restore():
                for item in lst.selectedItems():
                    key=item.data(Qt.ItemDataRole.UserRole);self.hidden.discard(key);self.disabled.discard(key)
                refill();self.refresh();self.save_preferences()
            lst.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection);layout.addWidget(self.button('Επαναφορά επιλεγμένων',restore));refill();d.exec()
        def eventFilter(self,obj,event):
            if event.type()==QEvent.Type.Show and isinstance(obj,(BaseDialog,QMenu)) and hasattr(self,'overlay'):self.overlay.hide()
            if event.type()==QEvent.Type.KeyPress and not app.activeModalWidget() and not app.activePopupWidget():self.show_hud()
            return super().eventFilter(obj,event)
        def show_hud(self):
            if self.closing:return
            self.last_activity=time.monotonic();self.set_hud_visible(True)
        def apply_overlay_style(self):
            alpha=round(255*self.overlay_opacity/100)
            # The native video stays opaque; only the separate HUD surface has alpha.
            self.overlay.setStyleSheet(f'QWidget#videoHUD {{background:transparent;}} QFrame#panel {{background:rgba(12,22,36,{alpha});border:1px solid rgba(115,160,180,90);border-radius:10px;}} QLabel {{color:#f2f7fc;background:transparent;}} QPushButton {{background:rgba(25,43,63,{alpha});color:#f0f5fa;border:1px solid rgba(100,140,165,110);}}')
        def position_overlay(self):
            if not self.isVisible() or self.isMinimized():self.overlay.hide();return
            width=max(350,self.video.width()-32);self.overlay.setFixedWidth(width);self.overlay.adjustSize()
            point=self.video.mapToGlobal(self.video.rect().bottomLeft());self.overlay.move(point.x()+16,point.y()-self.overlay.height()-16)
        def resizeEvent(self,event):
            super().resizeEvent(event)
            if hasattr(self,'overlay'):QTimer.singleShot(0,self.position_overlay)
        def moveEvent(self,event):
            super().moveEvent(event)
            if hasattr(self,'overlay'):self.position_overlay()
        def set_hud_visible(self,visible):
            self.hud_visible=visible;self.header_widget.setVisible(visible and not self.full);self.notice.setVisible(visible and not self.full)
            self.sidebar.setVisible(visible and self.sidebar_open and not self.full);self.controls.setVisible(visible);self.infobar.setVisible(visible)
            self.position_overlay()
            if visible and self.isVisible() and not self.isMinimized() and not self.closing and not app.activeModalWidget() and not app.activePopupWidget():self.overlay.show();self.overlay.raise_()
            else:self.overlay.hide()
        def check_hud(self):
            if self.closing or self.isMinimized() or not self.isVisible():self.overlay.hide();return
            if app.activePopupWidget() or app.activeModalWidget():self.overlay.hide();self.last_activity=time.monotonic();return
            if self.hud_visible and not self.overlay.isVisible():self.set_hud_visible(True)
            self.position_overlay()
            position=QCursor.pos()
            if position!=self.last_cursor:
                self.last_cursor=position
                if self.rect().contains(self.mapFromGlobal(position)):self.show_hud()
            if not self.auto_hide or self.current is None or not self.play_started:return
            if app.activePopupWidget() or app.activeModalWidget() or (not self.full and self.search.hasFocus()) or self.seek.isSliderDown():return
            if self.player and self.player.get_state() not in (vlc.State.Playing,vlc.State.Paused):return
            if time.monotonic()-self.last_activity>self.hide_delay:self.set_hud_visible(False)
        def toggle_auto_hide(self):
            self.auto_hide=not self.auto_hide;self.show_hud();self.save_preferences()
        def toggle_sidebar(self):
            self.sidebar_open=not self.sidebar_open;self.show_hud()
        def fullscreen(self):
            self.full=not self.full
            if self.full:
                self.search.clearFocus();self.video.setFocus();self.was_maximized=self.isMaximized();self.setMinimumSize(0,0);self.splitter.setHandleWidth(0);self.video_layout.removeWidget(self.controls);self.controls.setParent(self.overlay);self.overlay_layout.addWidget(self.controls)
                self.outer_layout.setContentsMargins(0,0,0,0);self.video.setStyleSheet('background:#000;border-radius:0;');self.header_widget.hide();self.sidebar.hide();self.notice.hide();self.showFullScreen()
            else:
                self.setMinimumSize(1100,650);self.splitter.setHandleWidth(4);self.overlay_layout.removeWidget(self.controls);self.controls.setParent(self.video_layout.parentWidget());self.video_layout.addWidget(self.controls);self.outer_layout.setContentsMargins(12,10,12,10);self.video.setStyleSheet('background:#000;border-radius:10px;')
                if getattr(self,'was_maximized',False):self.showMaximized()
                else:self.showNormal()
            self.show_hud();QTimer.singleShot(100,self.position_overlay)
        def exit_fullscreen(self):
            if self.full:self.fullscreen()
        def playback_menu(self):
            m=QMenu(self)
            aspect=m.addMenu('Aspect ratio')
            for label,value in [('Auto',None),('16:9','16:9'),('4:3','4:3')]:aspect.addAction(label,lambda v=value:self.player.video_set_aspect_ratio(v) if self.player else None)
            audio=m.addMenu('Audio tracks');subs=m.addMenu('Subtitles')
            if self.player:
                for tid,name in self.player.audio_get_track_description() or []:
                    label=name.decode(errors='replace') if isinstance(name,bytes) else str(name);audio.addAction(label,lambda t=tid:self.player.audio_set_track(t))
                for tid,name in self.player.video_get_spu_description() or []:
                    label=name.decode(errors='replace') if isinstance(name,bytes) else str(name);subs.addAction(label,lambda t=tid:self.player.video_set_spu(t))
            m.addAction('Snapshot',self.snapshot)
            if self.current is not None:
                source_menu=m.addMenu('Πηγές καναλιού')
                for i,s in enumerate(self.channels[self.current].sources):source_menu.addAction(f'Πηγή {i+1} • {s.state}',lambda n=i:self.play_channel(self.current,n))
            m.exec(self.controls.mapToGlobal(self.controls.rect().topLeft()))
        def snapshot(self):
            if not self.player or self.current is None:return
            self.rec_folder.mkdir(parents=True,exist_ok=True);p=self.rec_folder/('Snapshot_'+time.strftime('%Y%m%d_%H%M%S')+'.png')
            rc=self.player.video_take_snapshot(0,str(p),0,0);self.notice.setText('Snapshot αποθηκεύτηκε' if rc==0 else 'Δεν υπάρχει ενεργό video για snapshot')
        def info(self):
            d=QDialog(self);d.setWindowTitle('Info • Κατάσταση καναλιών');d.resize(900,600);layout=QVBoxLayout(d);layout.addWidget(QLabel(getattr(self,'summary_text',self.summary.text())+f'  •  Hidden {len(self.hidden)}  •  Disabled {len(self.disabled)}'))
            text=QLabel('On Air = διαθέσιμη πηγή στον τελευταίο έλεγχο (ενδέχεται να είναι αποθηκευμένος). Δεν εγγυάται εικόνα, γεωγραφική πρόσβαση ή διάρκεια λειτουργίας.\nΤα totals μετρούν μοναδικά κανάλια, όχι εναλλακτικές πηγές. Pending = δεν ολοκληρώθηκε ο έλεγχος.');text.setWordWrap(True);layout.addWidget(text)
            table=QTableWidget(len(self.channels),4);table.setHorizontalHeaderLabels([tr(x) for x in ['Κανάλι','Κατηγορία','Κατάσταση','Πηγές / διάγνωση']]);table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            for i,c in enumerate(self.channels):
                values=[c.name,c.group,('Disabled' if c.key in self.disabled else c.state)+(' / Hidden' if c.key in self.hidden else ''),' | '.join(f'{n+1}: {s.state} — {s.reason}' for n,s in enumerate(c.sources))]
                for col,value in enumerate(values):table.setItem(i,col,QTableWidgetItem(tr(value) if col in (2,3) else value))
            table.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeMode.Stretch);table.resizeColumnsToContents();layout.addWidget(table)
            note=QLabel('REC: '+str(self.rec_folder)+'\nCache / temp: καθαρισμός μόνο των φακέλων της εφαρμογής σε κάθε εκκίνηση.');note.setWordWrap(True);layout.addWidget(note);d.exec()
        def about(self):
            self.show_hud();d=QDialog(self);d.setWindowTitle('About • TVBro');d.resize(590,470);layout=QVBoxLayout(d)
            title=QLabel('TVBro '+VERSION);title.setStyleSheet('font-size:24px;font-weight:700;color:#329ca5;');layout.addWidget(title);layout.addWidget(QLabel('Your live TV buddy.'))
            description=QLabel(tr('Εφαρμογή IPTV με ενσωματωμένο VLC, M3U / Xtream Codes, έλεγχο πηγών, ομάδες αγαπημένων και εγγραφή ζωντανών ροών.'));description.setWordWrap(True);layout.addWidget(description)
            profile=QLabel('<b>ALU DEV TEAM @ 2026</b><br>Nikolaos K. Paridis シ (nikkpap)<br><br><a href="mailto:nikkpap@gmail.com">nikkpap@gmail.com</a><br><a href="https://t.me/TVBro">Telegram — TVBro</a><br><a href="https://github.com/nikkpap/TVBro">GitHub — TVBro</a>');profile.setOpenExternalLinks(True);layout.addWidget(profile)
            discussion=QLabel(tr('Είμαστε ανοιχτοί σε συζητήσεις και ιδέες. Ένα δημόσιο brainstorming είναι καλύτερο από καθόλου brainstorming :) Στην υγειά μας!'));discussion.setWordWrap(True);layout.addWidget(discussion)
            controls=QLabel(tr('Space: Pause • L: Go Live • R: REC • M: Mute • F: Fullscreen\nCtrl+B: Κανάλια • Ctrl+I: Info • Esc: Exit fullscreen\nREC επανασυνδέει τη ροή. Pause/seek εξαρτώνται από το stream.\nAuto-hide: χρόνος από τις Ρυθμίσεις, επιστροφή με κίνηση ποντικιού.'));controls.setWordWrap(True);layout.addWidget(controls)
            layout.addStretch();layout.addWidget(self.button('Κλείσιμο',d.accept));d.exec()
        def tick(self):
            self.clock.setText(time.strftime('%H:%M:%S'))
            if not self.player or self.current is None:return
            state=self.player.get_state();now=time.monotonic();c=self.channels[self.current]
            self.pause_button.setText('▶ Resume' if state==vlc.State.Paused else 'Ⅱ Pause')
            resolution=self.player.video_get_size(0) or (0,0);w,h=resolution
            seekable=bool(self.player.is_seekable());self.seek.setEnabled(seekable)
            if not self.seek.isSliderDown():self.seek.setValue(max(0,int(self.player.get_position()*1000)))
            def fmt(ms):
                secs=max(0,ms//1000);return f'{secs//60:02d}:{secs%60:02d}'
            self.elapsed.setText(fmt(self.player.get_time()));length=self.player.get_length();self.duration.setText(fmt(length) if length>0 else 'LIVE')
            self.stream_label.setText(f'{str(state).split(".")[-1].upper()}  •  {c.group}  •  Πηγή {self.source_index+1}/{len(c.sources)}  •  {str(w)+"×"+str(h) if w else "—"}  •  '+('Timeshift διαθέσιμο' if seekable else 'LIVE'))
            if self.recording:
                try:size=self.record_path.stat().st_size
                except OSError:size=0
                self.rec_button.setText('● REC '+fmt(int((now-self.rec_started)*1000)))
                self.notice.setText(f'VLC REC • {size/1048576:.1f} MB • {self.record_path.name}'+(' • Αναμονή δεδομένων…' if size==0 else ''))
                if now-self.rec_started>25 and size==0 and not self.rec_wait_failed:
                    self.rec_wait_failed=True;self.finish_recording();return
            if self.play_started and ((state in (vlc.State.Error,vlc.State.Ended)) or (now-self.play_started>22 and state in (vlc.State.Opening,vlc.State.Buffering))):
                was_recording=self.recording
                if was_recording:self.finish_recording(restart=False)
                c.sources[self.source_index].state='offline';c.sources[self.source_index].reason='Αποτυχία αναπαραγωγής VLC';self.refresh()
                remaining=[i for i,s in enumerate(c.sources) if i not in self.tried and s.state=='online']
                if remaining:
                    self.play_channel(self.current,remaining[0]);self.notice.setText('Δοκιμή εναλλακτικής πηγής'+(' • Η εγγραφή σταμάτησε' if was_recording else ''))
                else:self.play_started=0;self.notice.setText('Η αναπαραγωγή απέτυχε. Κάνε νέο έλεγχο ή διάλεξε άλλη πηγή.')
        def closeEvent(self,event):
            event.ignore()
            if self.closing:return
            self.closing=True;self.timer.stop();self.hud_timer.stop();self.catalog_timer.stop();self.cancel_scan();self.load_generation+=1
            self.save_catalog();self.save_preferences();self.overlay.hide();self.hide()
            self.shutdown_done=threading.Event();self.shutdown_started=time.monotonic()
            player=self.player
            def shutdown():
                try:
                    if player:player.stop();player.release()
                    if engine:engine.release()
                finally:self.shutdown_done.set()
            # libVLC stop can wait on a stalled network input: never block Qt.
            threading.Thread(target=shutdown,name='VLC shutdown',daemon=True).start()
            self.close_timer=QTimer(self);self.close_timer.timeout.connect(self.retry_close);self.close_timer.start(100)
        def retry_close(self):
            settled=self.shutdown_done.is_set() and not any(w.isRunning() for w in self.workers+self.loaders)
            if not settled and time.monotonic()-self.shutdown_started<8:return
            self.close_timer.stop()
            for folder in (root/'cache',temp_root):
                try:shutil.rmtree(folder)
                except OSError:pass
            lock.unlock()
            if settled:app.quit()
            else:
                # Settings/status already saved. Bound shutdown if native VLC or
                # a network worker never returns; OS releases remaining resources.
                os._exit(0)

    win=Window();win.show()
    if demo:
        def populate():
            win.cancel_scan()
            for i,c in enumerate(win.channels):
                for s in c.sources:s.state='online' if i%3 else 'offline';s.reason='Demo only'
            win.scan_total=win.scan_done=sum(len(c.sources) for c in win.channels);win.refresh();win.channel_number.setText('004');win.channel_title.setText('ΑΝΤ1');win.stream_label.setText('LIVE  •  Πανελλαδικά  •  1920×1080  •  Πηγή 1/2');win.notice.setText('UI preview • demo data, no playback or broadcast test')
            win.position_overlay();preview=win.grab();painter=QPainter(preview);painter.drawPixmap(win.mapFromGlobal(win.overlay.pos()),win.overlay.grab());painter.end();preview.save(str(Path(__file__).parent/'UI_Preview.png'))
            QTimer.singleShot(300,win.close)
        QTimer.singleShot(1500,populate)
    app.exec()

if __name__=='__main__':
    try:launch()
    except Exception as exc:
        if os.name=='nt':
            import ctypes
            ctypes.windll.user32.MessageBoxW(None,'Δεν μπόρεσε να ξεκινήσει το TVBro.\n'+type(exc).__name__+'\nΕκτέλεσε Install_Dependencies.bat και έλεγξε VLC / Python 64-bit.','TVBro',16)
        else:raise
