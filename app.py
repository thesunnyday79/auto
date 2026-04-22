import streamlit as st
import os
import re
import subprocess
import tempfile
import shutil
import zipfile
import io
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Auto Render Video – Full Length",
    page_icon="🎬",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0f0f0f;
    color: #e8e8e0;
    font-family: 'IBM Plex Sans', sans-serif;
}
[data-testid="stAppViewContainer"] { background: #0f0f0f; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }

.title-bar {
    background: #1a1a1a;
    border: 1px solid #2e2e2e;
    border-left: 3px solid #ff6b35;
    padding: 10px 20px;
    margin-bottom: 24px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ff6b35;
}

.row-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    padding-top: 8px;
}

.file-info-box {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 2px;
    padding: 8px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #ccc;
    min-height: 38px;
    display: flex;
    align-items: center;
    word-break: break-all;
}

.row-divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 8px 0;
}

.badge-yt  { background:#ff0000;color:#fff;padding:2px 6px;border-radius:2px;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;margin-right:6px; }
.badge-gd  { background:#1a73e8;color:#fff;padding:2px 6px;border-radius:2px;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;margin-right:6px; }
.badge-url { background:#4caf50;color:#fff;padding:2px 6px;border-radius:2px;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;margin-right:6px; }
.badge-file{ background:#555;color:#fff;padding:2px 6px;border-radius:2px;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:600;margin-right:6px; }

.link-panel {
    background: #111;
    border: 1px solid #222;
    border-top: 2px solid #ff6b35;
    padding: 14px 16px;
    margin-top: 6px;
    border-radius: 0 0 2px 2px;
}

.link-hint {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #444;
    margin-top: 8px;
    line-height: 1.7;
}

.status-box {
    background: #0d1a0d;
    border: 1px solid #1a3a1a;
    border-left: 3px solid #4caf50;
    padding: 12px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #4caf50;
    margin-top: 16px;
}
.status-box.error  { background:#1a0d0d;border-color:#3a1a1a;border-left-color:#f44336;color:#f44336; }
.status-box.warning{ background:#1a1500;border-color:#3a3000;border-left-color:#ff9800;color:#ff9800; }

.stButton > button {
    background: #1e1e1e !important;
    color: #ccc !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    padding: 6px 14px !important;
    transition: all 0.15s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover { background:#ff6b35 !important;color:#fff !important;border-color:#ff6b35 !important; }

.link-btn > button { border-color:#ff6b35 !important;color:#ff6b35 !important; }
.link-btn > button:hover { background:#ff6b35 !important;color:#fff !important; }

.render-btn > button {
    background: #ff6b35 !important;
    color: #fff !important;
    border-color: #ff6b35 !important;
    width: 100% !important;
    padding: 10px 20px !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
}
.render-btn > button:hover { background:#e55a25 !important;border-color:#e55a25 !important; }

.stRadio > div { flex-direction: row !important; gap: 20px; }
.stRadio label { font-family:'IBM Plex Mono',monospace !important;font-size:11px !important;color:#aaa !important; }

[data-testid="stFileUploader"] { background:#141414 !important;border:1px dashed #2a2a2a !important;border-radius:2px !important; }
[data-testid="stFileUploader"] label { font-family:'IBM Plex Mono',monospace !important;font-size:11px !important;color:#555 !important; }

.stTextInput > div > div > input {
    background:#1a1a1a !important;border:1px solid #2a2a2a !important;border-radius:2px !important;
    color:#ccc !important;font-family:'IBM Plex Mono',monospace !important;font-size:12px !important;
}
.stTextArea textarea {
    background:#111 !important;border:1px solid #2a2a2a !important;border-radius:2px !important;
    color:#aaa !important;font-family:'IBM Plex Mono',monospace !important;font-size:11px !important;
}

.stProgress > div > div { background:#ff6b35 !important; }

.stSelectbox > div > div {
    background:#1a1a1a !important;border:1px solid #2a2a2a !important;border-radius:2px !important;
    color:#ccc !important;font-family:'IBM Plex Mono',monospace !important;
}

.log-area {
    background:#0a0a0a;border:1px solid #1e1e1e;padding:12px;
    font-family:'IBM Plex Mono',monospace;font-size:11px;color:#666;
    max-height:220px;overflow-y:auto;line-height:1.6;white-space:pre-wrap;
}
.log-line-ok   { color:#4caf50; }
.log-line-err  { color:#f44336; }
.log-line-info { color:#888; }
.log-line-dl   { color:#1a73e8; }

/* Download buttons */
[data-testid="stDownloadButton"] > button {
    background: #0d1a0d !important;
    color: #4caf50 !important;
    border: 1px solid #1a3a1a !important;
    border-left: 3px solid #4caf50 !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    padding: 8px 16px !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #4caf50 !important;
    color: #000 !important;
    border-color: #4caf50 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State ────────────────────────────────────────────────────────────
def ss(k, d):
    if k not in st.session_state: st.session_state[k] = d

ss("video_files", [])
ss("video_folder", "")
ss("video_links", [])          # list of dicts: {url, source, name}
ss("rendered_files", [])       # list of paths to finished output files
ss("logo_file", None)
ss("music_file", None)
ss("music_folder", "")
ss("output_folder", "")
ss("logo_mode", "Đứng yên góc")
ss("music_mode", "Giữ nhạc gốc")
ss("log_lines", [])
ss("show_video_file", False)
ss("show_video_folder", False)
ss("show_link_panel", False)
ss("show_logo", False)
ss("show_music", False)
ss("show_music_folder", False)
ss("show_output", False)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def add_log(msg, kind="info"):
    st.session_state.log_lines.append((msg, kind))

def check_ffmpeg():  return shutil.which("ffmpeg") is not None
def check_ytdlp():   return shutil.which("yt-dlp") is not None

def format_size(path):
    try:
        size = os.path.getsize(path)
        for u in ["B","KB","MB","GB"]:
            if size < 1024: return f"{size:.1f} {u}"
            size /= 1024
        return f"{size:.1f} GB"
    except: return ""

def format_size_bytes(size):
    for u in ["B","KB","MB","GB"]:
        if size < 1024: return f"{size:.1f} {u}"
        size /= 1024
    return f"{size:.1f} GB"

def detect_link_source(url: str) -> str:
    url = url.strip()
    if re.search(r"(youtube\.com/watch|youtu\.be/|youtube\.com/shorts)", url):
        return "youtube"
    if re.search(r"drive\.google\.com", url):
        return "gdrive"
    return "direct"

def gdrive_direct(url: str) -> str:
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if m: return f"https://drive.google.com/uc?export=download&id={m.group(1)}&confirm=t"
    m2 = re.search(r"id=([a-zA-Z0-9_-]+)", url)
    if m2: return f"https://drive.google.com/uc?export=download&id={m2.group(1)}&confirm=t"
    return url

def source_badge(src: str) -> str:
    return {"youtube":'<span class="badge-yt">YT</span>',
            "gdrive": '<span class="badge-gd">GD</span>',
            "direct": '<span class="badge-url">URL</span>',
            "file":   '<span class="badge-file">FILE</span>'}.get(src,"")

def download_link_to_tmp(link_info: dict):
    url    = link_info["url"]
    source = link_info["source"]
    name   = link_info.get("name","video")

    if source == "youtube":
        if not check_ytdlp():
            raise RuntimeError("yt-dlp chưa được cài. Chạy: pip install yt-dlp")
        tmp_dir  = tempfile.mkdtemp()
        out_tmpl = os.path.join(tmp_dir, "%(title)s.%(ext)s")
        cmd = ["yt-dlp","-f","bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
               "--merge-output-format","mp4","-o", out_tmpl, url]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if res.returncode != 0:
            raise RuntimeError(res.stderr[-300:])
        files = list(Path(tmp_dir).glob("*.mp4"))
        if not files: raise RuntimeError("yt-dlp không tạo được file mp4")
        return str(files[0]), files[0].stem or name

    elif source == "gdrive":
        direct_url = gdrive_direct(url)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4"); tmp.close()
        res = subprocess.run(["curl","-L","-o",tmp.name, direct_url],
                             capture_output=True, text=True, timeout=600)
        if res.returncode != 0: raise RuntimeError(res.stderr[-200:])
        return tmp.name, name or "gdrive_video"

    else:  # direct URL
        suffix = Path(url.split("?")[0]).suffix or ".mp4"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix); tmp.close()
        res = subprocess.run(["curl","-L","-o",tmp.name, url],
                             capture_output=True, text=True, timeout=600)
        if res.returncode != 0: raise RuntimeError(res.stderr[-200:])
        return tmp.name, Path(url.split("?")[0]).stem or name or "video"


# ─── UI ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="title-bar">⬛ AUTO RENDER VIDEO — FULL LENGTH</div>', unsafe_allow_html=True)

col_main, col_side = st.columns([3, 1], gap="large")

with col_main:

    # ══════════════════════════════════════════════════════
    # VIDEO ROW
    # ══════════════════════════════════════════════════════
    st.markdown('<div class="row-label">VIDEO</div>', unsafe_allow_html=True)

    v1, v2, v3, v4 = st.columns([4, 1, 1, 1])

    with v1:
        parts = []
        if st.session_state.video_files:
            parts.append(f"{len(st.session_state.video_files)} file(s)")
        if st.session_state.video_folder:
            parts.append(f"📁 {st.session_state.video_folder}")
        if st.session_state.video_links:
            yt = sum(1 for l in st.session_state.video_links if l["source"]=="youtube")
            gd = sum(1 for l in st.session_state.video_links if l["source"]=="gdrive")
            ur = sum(1 for l in st.session_state.video_links if l["source"]=="direct")
            tags = []
            if yt: tags.append(f'<span class="badge-yt">YT ×{yt}</span>')
            if gd: tags.append(f'<span class="badge-gd">GD ×{gd}</span>')
            if ur: tags.append(f'<span class="badge-url">URL ×{ur}</span>')
            parts.append(" ".join(tags))
        display_text = " · ".join(parts) if parts else "<span style='color:#333'>No video selected</span>"
        st.markdown(f'<div class="file-info-box">{display_text}</div>', unsafe_allow_html=True)

    with v2:
        if st.button("FILE", key="btn_vf"):
            st.session_state.show_video_file   = not st.session_state.show_video_file
            st.session_state.show_video_folder = False
            st.session_state.show_link_panel   = False

    with v3:
        if st.button("FOLDER", key="btn_vd"):
            st.session_state.show_video_folder = not st.session_state.show_video_folder
            st.session_state.show_video_file   = False
            st.session_state.show_link_panel   = False

    with v4:
        st.markdown('<div class="link-btn">', unsafe_allow_html=True)
        if st.button("LINK", key="btn_vl"):
            st.session_state.show_link_panel   = not st.session_state.show_link_panel
            st.session_state.show_video_file   = False
            st.session_state.show_video_folder = False
        st.markdown('</div>', unsafe_allow_html=True)

    # File uploader
    if st.session_state.show_video_file:
        up = st.file_uploader("Video files", type=["mp4","mov","avi","mkv","wmv","flv"],
                              accept_multiple_files=True, key="video_uploader",
                              label_visibility="collapsed")
        if up:
            st.session_state.video_files  = up
            st.session_state.video_folder = ""

    # Folder path
    if st.session_state.show_video_folder:
        fp = st.text_input("Folder path", placeholder="/path/to/videos",
                           key="video_folder_input", label_visibility="collapsed")
        if fp:
            st.session_state.video_folder = fp
            st.session_state.video_files  = []

    # ── LINK PANEL ──────────────────────────────────────────────────────────
    if st.session_state.show_link_panel:
        st.markdown('<div class="link-panel">', unsafe_allow_html=True)

        lc1, lc2 = st.columns([5, 1])
        with lc1:
            new_link = st.text_input(
                "Link input",
                placeholder="https://youtube.com/watch?v=...  |  https://drive.google.com/...  |  https://example.com/video.mp4",
                key="link_input",
                label_visibility="collapsed",
            )
        with lc2:
            add_btn = st.button("➕ ADD", key="btn_add_link")

        if add_btn and new_link.strip():
            url = new_link.strip()
            src = detect_link_source(url)
            nm  = url.split("/")[-1].split("?")[0] or f"link_{len(st.session_state.video_links)+1}"
            st.session_state.video_links.append({"url": url, "source": src, "name": nm})
            st.rerun()

        # Bulk paste
        with st.expander("📋  Dán nhiều link (mỗi link 1 dòng)"):
            bulk = st.text_area("Bulk links",
                                placeholder="https://youtu.be/abc\nhttps://drive.google.com/...\nhttps://example.com/vid.mp4",
                                label_visibility="collapsed", height=90, key="bulk_input")
            if st.button("ADD ALL", key="btn_bulk"):
                for line in bulk.strip().splitlines():
                    line = line.strip()
                    if line:
                        src = detect_link_source(line)
                        nm  = line.split("/")[-1].split("?")[0] or f"link_{len(st.session_state.video_links)+1}"
                        st.session_state.video_links.append({"url": line, "source": src, "name": nm})
                st.rerun()

        # Link list
        if st.session_state.video_links:
            st.markdown('<div style="margin-top:10px">', unsafe_allow_html=True)
            to_rm = []
            for i, lk in enumerate(st.session_state.video_links):
                rc1, rc2 = st.columns([10, 1])
                with rc1:
                    short = lk["url"][:72] + "…" if len(lk["url"]) > 72 else lk["url"]
                    st.markdown(
                        f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:#666;'
                        f'padding:5px 0;border-bottom:1px solid #1a1a1a">'
                        f'{source_badge(lk["source"])}{short}</div>',
                        unsafe_allow_html=True
                    )
                with rc2:
                    if st.button("✕", key=f"rm_{i}"): to_rm.append(i)
            for i in sorted(to_rm, reverse=True):
                st.session_state.video_links.pop(i)
            if to_rm: st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="link-hint">
        <span class="badge-yt">YT</span> YouTube · watch / shorts / youtu.be &nbsp;|&nbsp;
        <span class="badge-gd">GD</span> Google Drive · /d/FILE_ID/view &nbsp;|&nbsp;
        <span class="badge-url">URL</span> URL trực tiếp · .mp4 .mov .mkv ...<br>
        ⚠ Cần <b>yt-dlp</b> cho YouTube &nbsp;·&nbsp; <b>curl</b> cho Drive &amp; URL trực tiếp
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # LOGO ROW
    # ══════════════════════════════════════════════════════
    st.markdown('<div class="row-label">LOGO</div>', unsafe_allow_html=True)
    l1, l2, l3 = st.columns([2, 1, 2])
    with l1:
        ld = st.session_state.logo_file.name if st.session_state.logo_file else "<span style='color:#333'>No logo selected</span>"
        st.markdown(f'<div class="file-info-box">{ld}</div>', unsafe_allow_html=True)
    with l2:
        if st.button("LOGO FILE", key="btn_logo"):
            st.session_state.show_logo = not st.session_state.show_logo
    with l3:
        lm = st.radio("Logo Mode", ["Đứng yên góc","Chạy viền trên"],
                      key="logo_mode_radio", horizontal=True, label_visibility="collapsed")
        st.session_state.logo_mode = lm
    if st.session_state.show_logo:
        lf = st.file_uploader("Logo", type=["png","jpg","jpeg","gif","webp"],
                              key="logo_uploader", label_visibility="collapsed")
        if lf: st.session_state.logo_file = lf

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # MUSIC ROW
    # ══════════════════════════════════════════════════════
    st.markdown('<div class="row-label">MUSIC</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns([2, 1, 2, 1])
    with m1:
        if st.session_state.music_file:   md = st.session_state.music_file.name
        elif st.session_state.music_folder: md = st.session_state.music_folder
        else: md = "<span style='color:#333'>No music selected</span>"
        st.markdown(f'<div class="file-info-box">{md}</div>', unsafe_allow_html=True)
    with m2:
        if st.button("MUSIC FILE", key="btn_music"):
            st.session_state.show_music = not st.session_state.show_music
            st.session_state.show_music_folder = False
    with m3:
        mm = st.radio("Music Mode", ["Giữ nhạc gốc","Thay nhạc"],
                      key="music_mode_radio", horizontal=True, label_visibility="collapsed")
        st.session_state.music_mode = mm
    with m4:
        if st.button("FOLDER", key="btn_mf"):
            st.session_state.show_music_folder = not st.session_state.show_music_folder
            st.session_state.show_music = False
    if st.session_state.show_music:
        mf = st.file_uploader("Music", type=["mp3","wav","aac","flac","ogg","m4a"],
                              key="music_uploader", label_visibility="collapsed")
        if mf: st.session_state.music_file = mf
    if st.session_state.show_music_folder:
        mfp = st.text_input("Music folder", placeholder="/path/to/music",
                            key="music_folder_input", label_visibility="collapsed")
        if mfp: st.session_state.music_folder = mfp

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # OUTPUT ROW
    # ══════════════════════════════════════════════════════
    st.markdown('<div class="row-label">OUTPUT</div>', unsafe_allow_html=True)
    o1, o2 = st.columns([5, 1])
    with o1:
        od = st.session_state.output_folder or "<span style='color:#333'>No output folder selected</span>"
        st.markdown(f'<div class="file-info-box">{od}</div>', unsafe_allow_html=True)
    with o2:
        if st.button("BROWSE", key="btn_out"):
            st.session_state.show_output = not st.session_state.show_output
    if st.session_state.show_output:
        ofp = st.text_input("Output folder", placeholder="/path/to/output",
                            key="output_folder_input", label_visibility="collapsed")
        if ofp: st.session_state.output_folder = ofp

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ── Options ──────────────────────────────────────────────────────────────
    with st.expander("⚙  OPTIONS", expanded=False):
        oc1, oc2, oc3 = st.columns(3)
        with oc1:
            st.selectbox("Vị trí logo", ["Góc trên trái","Góc trên phải","Góc dưới trái","Góc dưới phải","Giữa"], key="logo_position")
            st.slider("Kích thước logo (%)", 5, 30, 15, key="logo_scale")
        with oc2:
            st.selectbox("Chất lượng video", ["Cao (CRF 18)","Trung bình (CRF 23)","Thấp (CRF 28)"], key="video_quality")
            st.selectbox("Video Codec", ["libx264 (H.264)","libx265 (H.265)","copy (giữ nguyên)"], key="video_codec")
        with oc3:
            st.slider("Âm lượng nhạc nền (%)", 0, 200, 100, key="audio_volume")
            st.slider("Âm lượng nhạc gốc (%)", 0, 200, 100, key="orig_volume")

    # ── Render Button ────────────────────────────────────────────────────────
    st.markdown("")
    rc1, rc2, rc3 = st.columns([1, 2, 1])
    with rc2:
        st.markdown('<div class="render-btn">', unsafe_allow_html=True)
        render_clicked = st.button("▶  START RENDER", key="btn_render")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Log ──────────────────────────────────────────────────────────────────
    if st.session_state.log_lines:
        log_html = '<div class="log-area">'
        for line, kind in st.session_state.log_lines[-40:]:
            css = {"ok":"log-line-ok","err":"log-line-err","info":"log-line-info","dl":"log-line-dl"}.get(kind,"log-line-info")
            log_html += f'<div class="{css}">{line}</div>'
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)

    # ── Download Panel ────────────────────────────────────────────────────────
    done_files = [p for p in st.session_state.rendered_files if os.path.exists(p)]
    if done_files:
        st.markdown('<hr class="row-divider" style="margin-top:16px">', unsafe_allow_html=True)
        st.markdown('<div class="row-label" style="margin-bottom:10px">⬇ DOWNLOAD</div>', unsafe_allow_html=True)

        if len(done_files) == 1:
            # Single file – direct download button
            fpath = done_files[0]
            fname = Path(fpath).name
            with open(fpath, "rb") as f:
                data = f.read()
            st.download_button(
                label=f"⬇  {fname}  ({format_size(fpath)})",
                data=data,
                file_name=fname,
                mime="video/mp4",
                key="dl_single",
                use_container_width=True,
            )
        else:
            # Multiple files – individual buttons + ZIP all
            dl_cols = st.columns(min(len(done_files), 3))
            for i, fpath in enumerate(done_files):
                fname = Path(fpath).name
                with open(fpath, "rb") as f:
                    data = f.read()
                with dl_cols[i % 3]:
                    st.download_button(
                        label=f"⬇ {fname[:28]}…" if len(fname) > 28 else f"⬇ {fname}",
                        data=data,
                        file_name=fname,
                        mime="video/mp4",
                        key=f"dl_{i}",
                        use_container_width=True,
                        help=f"{fname}  ·  {format_size(fpath)}",
                    )

            # ZIP all button
            st.markdown("")
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_STORED) as zf:
                for fpath in done_files:
                    zf.write(fpath, Path(fpath).name)
            zip_buf.seek(0)
            total_size = sum(os.path.getsize(p) for p in done_files)

            zc1, zc2, zc3 = st.columns([1, 2, 1])
            with zc2:
                st.download_button(
                    label=f"📦  DOWNLOAD ALL AS ZIP  ({format_size_bytes(total_size)})",
                    data=zip_buf.getvalue(),
                    file_name="rendered_videos.zip",
                    mime="application/zip",
                    key="dl_zip",
                    use_container_width=True,
                )


# ─── Side Panel ───────────────────────────────────────────────────────────────
with col_side:
    st.markdown('<div class="row-label" style="margin-bottom:12px">STATUS</div>', unsafe_allow_html=True)

    has_video  = bool(st.session_state.video_files or st.session_state.video_folder or st.session_state.video_links)
    has_output = bool(st.session_state.output_folder)
    has_logo   = st.session_state.logo_file is not None
    has_music  = bool(st.session_state.music_file or st.session_state.music_folder)
    ffmpeg_ok  = check_ffmpeg()
    ytdlp_ok   = check_ytdlp()
    has_yt     = any(l["source"]=="youtube" for l in st.session_state.video_links)

    def ind(ok, label):
        icon  = "●" if ok else "○"
        color = "#4caf50" if ok else "#444"
        return f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:{color};margin-bottom:6px">{icon} {label}</div>'

    st.markdown(
        ind(ffmpeg_ok, "FFmpeg") +
        ind(ytdlp_ok or not has_yt, "yt-dlp" + ("" if ytdlp_ok else " ⚠")) +
        ind(has_video,  "Video selected") +
        ind(has_logo,   "Logo selected") +
        ind(has_music,  "Music selected") +
        ind(has_output, "Output folder set"),
        unsafe_allow_html=True
    )

    if not ffmpeg_ok:
        st.markdown("""<div style="background:#1a0d0d;border:1px solid #3a1a1a;border-left:3px solid #f44336;
        padding:10px;font-family:IBM Plex Mono,monospace;font-size:10px;color:#f44336;margin-top:8px;line-height:1.7">
        ⚠ FFmpeg not found<br><code>sudo apt install ffmpeg</code><br>or<br><code>brew install ffmpeg</code>
        </div>""", unsafe_allow_html=True)

    if has_yt and not ytdlp_ok:
        st.markdown("""<div style="background:#1a1500;border:1px solid #3a3000;border-left:3px solid #ff9800;
        padding:10px;font-family:IBM Plex Mono,monospace;font-size:10px;color:#ff9800;margin-top:8px;line-height:1.7">
        ⚠ yt-dlp not found<br><code>pip install yt-dlp</code>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="row-divider" style="margin:16px 0">', unsafe_allow_html=True)
    st.markdown('<div class="row-label" style="margin-bottom:8px">QUEUE</div>', unsafe_allow_html=True)

    total_q = len(st.session_state.video_files) + (1 if st.session_state.video_folder else 0) + len(st.session_state.video_links)

    shown = 0
    for vf in st.session_state.video_files[:3]:
        st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#555;margin-bottom:3px">{source_badge("file")}{vf.name[:28]}</div>', unsafe_allow_html=True)
        shown += 1
    for lk in st.session_state.video_links[:max(0, 4-shown)]:
        short = lk["url"][:30] + "…" if len(lk["url"]) > 30 else lk["url"]
        st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#555;margin-bottom:3px">{source_badge(lk["source"])}{short}</div>', unsafe_allow_html=True)
        shown += 1
    if total_q == 0:
        st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#333">Empty queue</div>', unsafe_allow_html=True)
    elif total_q > shown:
        st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#444">... +{total_q-shown} more</div>', unsafe_allow_html=True)

    if st.button("CLEAR ALL", key="btn_clear"):
        for k, d in [("video_files",[]),("video_links",[]),("log_lines",[]),("rendered_files",[]),
                     ("logo_file",None),("music_file",None),
                     ("video_folder",""),("music_folder",""),("output_folder","")]:
            st.session_state[k] = d
        st.rerun()


# ─── Render Logic ─────────────────────────────────────────────────────────────
if render_clicked:
    errors = []
    has_any = bool(st.session_state.video_files or st.session_state.video_folder or st.session_state.video_links)
    if not has_any:
        errors.append("Chưa chọn video đầu vào")
    if not st.session_state.output_folder:
        errors.append("Chưa chọn thư mục output")
    if not check_ffmpeg():
        errors.append("FFmpeg chưa được cài đặt")
    if st.session_state.music_mode == "Thay nhạc" and not (st.session_state.music_file or st.session_state.music_folder):
        errors.append("Chế độ 'Thay nhạc' nhưng chưa chọn file nhạc")
    yt_links = [l for l in st.session_state.video_links if l["source"]=="youtube"]
    if yt_links and not check_ytdlp():
        errors.append("Có link YouTube nhưng yt-dlp chưa cài: pip install yt-dlp")

    if errors:
        for e in errors:
            st.markdown(f'<div class="status-box error">✗ {e}</div>', unsafe_allow_html=True)
    else:
        st.session_state.log_lines = []
        st.session_state.rendered_files = []   # reset previous downloads
        add_log("═══════════════════════════════════", "info")
        add_log("  RENDER SESSION STARTED", "ok")
        add_log("═══════════════════════════════════", "info")

        os.makedirs(st.session_state.output_folder, exist_ok=True)
        add_log(f"  OUTPUT → {st.session_state.output_folder}", "info")

        videos_to_process = []  # (src_path, display_name, is_tmp)

        # 1) Uploaded files
        for vf in st.session_state.video_files:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=Path(vf.name).suffix)
            tmp.write(vf.read()); tmp.close()
            videos_to_process.append((tmp.name, vf.name, True))

        # 2) Folder
        if st.session_state.video_folder and os.path.isdir(st.session_state.video_folder):
            for f in sorted(Path(st.session_state.video_folder).iterdir()):
                if f.suffix.lower() in {".mp4",".mov",".avi",".mkv",".wmv",".flv"}:
                    videos_to_process.append((str(f), f.name, False))

        # 3) Links – download
        dl_ph = st.empty()
        for i, lk in enumerate(st.session_state.video_links):
            src_label = {"youtube":"YouTube","gdrive":"Google Drive","direct":"URL"}.get(lk["source"],"Link")
            add_log(f"  ⬇ [{src_label}] {lk['url'][:65]}…", "dl")
            dl_ph.markdown(
                f'<div class="status-box" style="border-left-color:#1a73e8;color:#1a73e8">'
                f'⬇ Downloading {src_label} ({i+1}/{len(st.session_state.video_links)})…</div>',
                unsafe_allow_html=True
            )
            try:
                tmp_path, dname = download_link_to_tmp(lk)
                videos_to_process.append((tmp_path, dname, True))
                add_log(f"  ✓ Downloaded → {dname}", "ok")
            except Exception as ex:
                add_log(f"  ✗ Download failed: {str(ex)[:120]}", "err")
        dl_ph.empty()

        add_log(f"  TOTAL: {len(videos_to_process)} video(s)", "info")

        # Logo temp
        logo_tmp = None
        if st.session_state.logo_file:
            lt = tempfile.NamedTemporaryFile(delete=False, suffix=Path(st.session_state.logo_file.name).suffix)
            lt.write(st.session_state.logo_file.read()); lt.close()
            logo_tmp = lt.name
            add_log(f"  LOGO → {st.session_state.logo_file.name} ({st.session_state.logo_mode})", "info")

        # Music temp
        music_tmp = None
        if st.session_state.music_file and st.session_state.music_mode == "Thay nhạc":
            mt = tempfile.NamedTemporaryFile(delete=False, suffix=Path(st.session_state.music_file.name).suffix)
            mt.write(st.session_state.music_file.read()); mt.close()
            music_tmp = mt.name
        elif st.session_state.music_folder and st.session_state.music_mode == "Thay nhạc":
            for f in sorted(Path(st.session_state.music_folder).iterdir()):
                if f.suffix.lower() in {".mp3",".wav",".aac",".flac",".m4a"}:
                    music_tmp = str(f); break

        add_log("═══════════════════════════════════", "info")

        codec_map = {"libx264 (H.264)":"libx264","libx265 (H.265)":"libx265","copy (giữ nguyên)":"copy"}
        crf_map   = {"Cao (CRF 18)":18,"Trung bình (CRF 23)":23,"Thấp (CRF 28)":28}
        pos_map   = {"Góc trên trái":"10:10","Góc trên phải":"main_w-overlay_w-10:10",
                     "Góc dưới trái":"10:main_h-overlay_h-10","Góc dưới phải":"main_w-overlay_w-10:main_h-overlay_h-10",
                     "Giữa":"(main_w-overlay_w)/2:(main_h-overlay_h)/2"}

        codec    = codec_map.get(st.session_state.get("video_codec","libx264 (H.264)"),"libx264")
        crf      = crf_map.get(st.session_state.get("video_quality","Trung bình (CRF 23)"),23)
        logo_pos = pos_map.get(st.session_state.get("logo_position","Góc trên trái"),"10:10")
        logo_sc  = st.session_state.get("logo_scale",15)
        a_vol    = st.session_state.get("audio_volume",100)/100
        o_vol    = st.session_state.get("orig_volume",100)/100

        progress_bar = st.progress(0)
        total        = len(videos_to_process)
        status_ph    = st.empty()

        for idx, (src_path, orig_name, is_tmp) in enumerate(videos_to_process):
            stem     = Path(orig_name).stem
            out_path = os.path.join(st.session_state.output_folder, f"{stem}_rendered.mp4")
            add_log(f"  [{idx+1}/{total}] {orig_name}", "info")
            status_ph.markdown(f'<div class="status-box">⚙ Processing: {orig_name} ({idx+1}/{total})</div>', unsafe_allow_html=True)

            inputs  = ["-i", src_path]
            fc_parts = []
            last_v  = "[0:v]"
            last_a  = "[0:a]" if st.session_state.music_mode == "Giữ nhạc gốc" else None

            if logo_tmp:
                inputs += ["-i", logo_tmp]
                scale_e = f"iw*{logo_sc}/100:-1"
                if st.session_state.logo_mode == "Đứng yên góc":
                    fc_parts.append(f"[1:v]scale={scale_e}[logo];{last_v}[logo]overlay={logo_pos}[vout]")
                else:
                    fc_parts.append(f"[1:v]scale={scale_e}[logo];{last_v}[logo]overlay='if(gte(t,0),-overlay_w+t*100,NaN)':10[vout]")
                last_v = "[vout]"

            if music_tmp and st.session_state.music_mode == "Thay nhạc":
                mi = len(inputs) // 2
                inputs += ["-i", music_tmp]
                fc_parts.append(f"[0:a]volume={o_vol}[a0];[{mi}:a]volume={a_vol}[a1];[a0][a1]amix=inputs=2:duration=first[aout]")
                last_a = "[aout]"
            elif st.session_state.music_mode == "Giữ nhạc gốc" and o_vol != 1.0:
                fc_parts.append(f"[0:a]volume={o_vol}[aout]")
                last_a = "[aout]"

            cmd = ["ffmpeg", "-y"] + inputs
            if fc_parts:
                cmd += ["-filter_complex", ";".join(fc_parts), "-map", last_v]
                if last_a: cmd += ["-map", last_a]
            else:
                cmd += ["-map", "0:v"]
                if last_a: cmd += ["-map", "0:a"]

            if codec != "copy":
                cmd += ["-c:v", codec, "-crf", str(crf), "-preset", "fast"]
            else:
                cmd += ["-c:v", "copy"]
            cmd += ["-c:a","aac","-b:a","192k", out_path]

            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
                if res.returncode == 0:
                    add_log(f"  ✓ Done → {Path(out_path).name} ({format_size(out_path)})", "ok")
                    st.session_state.rendered_files.append(out_path)
                else:
                    add_log(f"  ✗ FFmpeg error: {(res.stderr or '').split(chr(10))[-3]}", "err")
            except subprocess.TimeoutExpired:
                add_log(f"  ✗ Timeout: {orig_name}", "err")
            except Exception as ex:
                add_log(f"  ✗ Exception: {str(ex)}", "err")

            if is_tmp and os.path.exists(src_path):
                try: os.unlink(src_path)
                except: pass

            progress_bar.progress((idx+1)/total)

        for tf in [logo_tmp, music_tmp]:
            if tf and tf.startswith(tempfile.gettempdir()) and os.path.exists(tf):
                try: os.unlink(tf)
                except: pass

        add_log("═══════════════════════════════════", "info")
        add_log("  ALL DONE", "ok")
        add_log("═══════════════════════════════════", "info")
        status_ph.markdown('<div class="status-box">✓ Render hoàn tất! Xem bên dưới để tải file.</div>', unsafe_allow_html=True)
        st.rerun()
