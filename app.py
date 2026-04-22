import streamlit as st
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import time

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

[data-testid="stAppViewContainer"] {
    background: #0f0f0f;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }

/* Main title bar */
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

/* Section labels */
.row-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    padding-top: 8px;
}

/* Custom file info box */
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

/* Divider */
.row-divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 8px 0;
}

/* Status box */
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

.status-box.error {
    background: #1a0d0d;
    border-color: #3a1a1a;
    border-left-color: #f44336;
    color: #f44336;
}

.status-box.warning {
    background: #1a1500;
    border-color: #3a3000;
    border-left-color: #ff9800;
    color: #ff9800;
}

/* Override Streamlit buttons */
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

.stButton > button:hover {
    background: #ff6b35 !important;
    color: #fff !important;
    border-color: #ff6b35 !important;
}

/* Primary render button */
.render-btn > button {
    background: #ff6b35 !important;
    color: #fff !important;
    border-color: #ff6b35 !important;
    width: 100% !important;
    padding: 10px 20px !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
}

.render-btn > button:hover {
    background: #e55a25 !important;
    border-color: #e55a25 !important;
}

/* Radio buttons */
.stRadio > div {
    flex-direction: row !important;
    gap: 20px;
}

.stRadio label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    color: #aaa !important;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background: #141414 !important;
    border: 1px dashed #2a2a2a !important;
    border-radius: 2px !important;
}

[data-testid="stFileUploader"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    color: #555 !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 2px !important;
    color: #ccc !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}

/* Progress bar */
.stProgress > div > div {
    background: #ff6b35 !important;
}

/* Select box */
.stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 2px !important;
    color: #ccc !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* Log area */
.log-area {
    background: #0a0a0a;
    border: 1px solid #1e1e1e;
    padding: 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #666;
    max-height: 200px;
    overflow-y: auto;
    line-height: 1.6;
    white-space: pre-wrap;
}

.log-line-ok { color: #4caf50; }
.log-line-err { color: #f44336; }
.log-line-info { color: #888; }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ──────────────────────────────────────────────────────
def ss(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

ss("video_files", [])
ss("video_folder", "")
ss("logo_file", None)
ss("music_file", None)
ss("music_folder", "")
ss("output_folder", "")
ss("logo_mode", "Đứng yên góc")
ss("music_mode", "Giữ nhạc gốc")
ss("log_lines", [])
ss("rendering", False)
ss("render_done", False)
ss("input_mode", "file")


# ─── Helpers ────────────────────────────────────────────────────────────────
def add_log(msg, kind="info"):
    st.session_state.log_lines.append((msg, kind))

def check_ffmpeg():
    return shutil.which("ffmpeg") is not None

def format_size(path):
    try:
        size = os.path.getsize(path)
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} GB"
    except:
        return ""


# ─── Title ───────────────────────────────────────────────────────────────────
st.markdown('<div class="title-bar">⬛ AUTO RENDER VIDEO — FULL LENGTH</div>', unsafe_allow_html=True)

# ─── Layout: Main panel ──────────────────────────────────────────────────────
col_main, col_side = st.columns([3, 1], gap="large")

with col_main:

    # ── VIDEO ROW ─────────────────────────────────────────────────────────
    st.markdown('<div class="row-label">VIDEO</div>', unsafe_allow_html=True)

    v_col1, v_col2, v_col3 = st.columns([4, 1, 1])
    with v_col1:
        video_display = ""
        if st.session_state.video_files:
            video_display = f"{len(st.session_state.video_files)} file(s) selected"
        elif st.session_state.video_folder:
            video_display = st.session_state.video_folder
        st.markdown(f'<div class="file-info-box">{video_display or "<span style=color:#333>No video selected</span>"}</div>', unsafe_allow_html=True)

    with v_col2:
        if st.button("FILE", key="btn_video_file"):
            st.session_state["show_video_file"] = not st.session_state.get("show_video_file", False)
            st.session_state["show_video_folder"] = False

    with v_col3:
        if st.button("FOLDER", key="btn_video_folder"):
            st.session_state["show_video_folder"] = not st.session_state.get("show_video_folder", False)
            st.session_state["show_video_file"] = False

    if st.session_state.get("show_video_file"):
        uploaded = st.file_uploader(
            "Chọn file video",
            type=["mp4", "mov", "avi", "mkv", "wmv", "flv"],
            accept_multiple_files=True,
            key="video_uploader",
            label_visibility="collapsed",
        )
        if uploaded:
            st.session_state.video_files = uploaded
            st.session_state.video_folder = ""

    if st.session_state.get("show_video_folder"):
        folder_path = st.text_input(
            "Đường dẫn folder chứa video",
            placeholder="/path/to/videos",
            key="video_folder_input",
            label_visibility="collapsed",
        )
        if folder_path:
            st.session_state.video_folder = folder_path
            st.session_state.video_files = []

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ── LOGO ROW ──────────────────────────────────────────────────────────
    st.markdown('<div class="row-label">LOGO</div>', unsafe_allow_html=True)

    l_col1, l_col2, l_col3 = st.columns([2, 1, 2])
    with l_col1:
        logo_display = ""
        if st.session_state.logo_file:
            logo_display = st.session_state.logo_file.name
        st.markdown(f'<div class="file-info-box">{logo_display or "<span style=color:#333>No logo selected</span>"}</div>', unsafe_allow_html=True)

    with l_col2:
        if st.button("LOGO FILE", key="btn_logo"):
            st.session_state["show_logo"] = not st.session_state.get("show_logo", False)

    with l_col3:
        st.markdown('<div style="padding-top:4px">', unsafe_allow_html=True)
        logo_mode = st.radio(
            "Logo Mode",
            ["Đứng yên góc", "Chạy viền trên"],
            key="logo_mode_radio",
            horizontal=True,
            label_visibility="collapsed",
        )
        st.session_state.logo_mode = logo_mode
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_logo"):
        logo_file = st.file_uploader(
            "Chọn file logo",
            type=["png", "jpg", "jpeg", "gif", "webp"],
            key="logo_uploader",
            label_visibility="collapsed",
        )
        if logo_file:
            st.session_state.logo_file = logo_file

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ── MUSIC ROW ─────────────────────────────────────────────────────────
    st.markdown('<div class="row-label">MUSIC</div>', unsafe_allow_html=True)

    m_col1, m_col2, m_col3, m_col4 = st.columns([2, 1, 2, 1])
    with m_col1:
        music_display = ""
        if st.session_state.music_file:
            music_display = st.session_state.music_file.name
        elif st.session_state.music_folder:
            music_display = st.session_state.music_folder
        st.markdown(f'<div class="file-info-box">{music_display or "<span style=color:#333>No music selected</span>"}</div>', unsafe_allow_html=True)

    with m_col2:
        if st.button("MUSIC FILE", key="btn_music"):
            st.session_state["show_music"] = not st.session_state.get("show_music", False)
            st.session_state["show_music_folder"] = False

    with m_col3:
        st.markdown('<div style="padding-top:4px">', unsafe_allow_html=True)
        music_mode = st.radio(
            "Music Mode",
            ["Giữ nhạc gốc", "Thay nhạc"],
            key="music_mode_radio",
            horizontal=True,
            label_visibility="collapsed",
        )
        st.session_state.music_mode = music_mode
        st.markdown('</div>', unsafe_allow_html=True)

    with m_col4:
        if st.button("FOLDER", key="btn_music_folder"):
            st.session_state["show_music_folder"] = not st.session_state.get("show_music_folder", False)
            st.session_state["show_music"] = False

    if st.session_state.get("show_music"):
        music_file = st.file_uploader(
            "Chọn file nhạc",
            type=["mp3", "wav", "aac", "flac", "ogg", "m4a"],
            key="music_uploader",
            label_visibility="collapsed",
        )
        if music_file:
            st.session_state.music_file = music_file

    if st.session_state.get("show_music_folder"):
        music_folder = st.text_input(
            "Đường dẫn folder nhạc",
            placeholder="/path/to/music",
            key="music_folder_input",
            label_visibility="collapsed",
        )
        if music_folder:
            st.session_state.music_folder = music_folder

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ── OUTPUT ROW ────────────────────────────────────────────────────────
    st.markdown('<div class="row-label">OUTPUT</div>', unsafe_allow_html=True)

    o_col1, o_col2 = st.columns([5, 1])
    with o_col1:
        output_display = st.session_state.output_folder
        st.markdown(f'<div class="file-info-box">{output_display or "<span style=color:#333>No output folder selected</span>"}</div>', unsafe_allow_html=True)

    with o_col2:
        if st.button("BROWSE", key="btn_output"):
            st.session_state["show_output"] = not st.session_state.get("show_output", False)

    if st.session_state.get("show_output"):
        output_folder = st.text_input(
            "Đường dẫn output folder",
            placeholder="/path/to/output",
            key="output_folder_input",
            label_visibility="collapsed",
        )
        if output_folder:
            st.session_state.output_folder = output_folder

    st.markdown('<hr class="row-divider">', unsafe_allow_html=True)

    # ── Additional Options ─────────────────────────────────────────────────
    with st.expander("⚙  OPTIONS", expanded=False):
        opt1, opt2, opt3 = st.columns(3)
        with opt1:
            logo_position = st.selectbox(
                "Vị trí logo",
                ["Góc trên trái", "Góc trên phải", "Góc dưới trái", "Góc dưới phải", "Giữa"],
                key="logo_position",
            )
            logo_scale = st.slider("Kích thước logo (%)", 5, 30, 15, key="logo_scale")
        with opt2:
            video_quality = st.selectbox(
                "Chất lượng video",
                ["Cao (CRF 18)", "Trung bình (CRF 23)", "Thấp (CRF 28)"],
                key="video_quality",
            )
            video_codec = st.selectbox(
                "Video Codec",
                ["libx264 (H.264)", "libx265 (H.265)", "copy (giữ nguyên)"],
                key="video_codec",
            )
        with opt3:
            audio_volume = st.slider("Âm lượng nhạc nền (%)", 0, 200, 100, key="audio_volume")
            original_volume = st.slider("Âm lượng nhạc gốc (%)", 0, 200, 100, key="orig_volume")

    # ── RENDER BUTTON ─────────────────────────────────────────────────────
    st.markdown("")
    render_col1, render_col2, render_col3 = st.columns([1, 2, 1])
    with render_col2:
        st.markdown('<div class="render-btn">', unsafe_allow_html=True)
        render_clicked = st.button("▶  START RENDER", key="btn_render")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── LOG OUTPUT ────────────────────────────────────────────────────────
    if st.session_state.log_lines:
        log_html = '<div class="log-area">'
        for line, kind in st.session_state.log_lines[-30:]:
            css = {"ok": "log-line-ok", "err": "log-line-err", "info": "log-line-info"}.get(kind, "log-line-info")
            log_html += f'<div class="{css}">{line}</div>'
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)


# ─── Side Panel: Status ───────────────────────────────────────────────────────
with col_side:
    st.markdown('<div class="row-label" style="margin-bottom:12px">STATUS</div>', unsafe_allow_html=True)

    has_video = bool(st.session_state.video_files or st.session_state.video_folder)
    has_output = bool(st.session_state.output_folder)
    has_logo = st.session_state.logo_file is not None
    has_music = bool(st.session_state.music_file or st.session_state.music_folder)
    ffmpeg_ok = check_ffmpeg()

    def indicator(ok, label):
        icon = "●" if ok else "○"
        color = "#4caf50" if ok else "#444"
        return f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:{color};margin-bottom:6px">{icon} {label}</div>'

    st.markdown(
        indicator(ffmpeg_ok, "FFmpeg installed") +
        indicator(has_video, "Video selected") +
        indicator(has_logo, "Logo selected") +
        indicator(has_music, "Music selected") +
        indicator(has_output, "Output folder set"),
        unsafe_allow_html=True
    )

    if not ffmpeg_ok:
        st.markdown("""
        <div style="background:#1a0d0d;border:1px solid #3a1a1a;border-left:3px solid #f44336;
        padding:10px;font-family:IBM Plex Mono,monospace;font-size:10px;color:#f44336;margin-top:8px;line-height:1.7">
        ⚠ FFmpeg not found.<br>
        Install:<br>
        <code>sudo apt install ffmpeg</code><br>or<br>
        <code>brew install ffmpeg</code>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="row-divider" style="margin:16px 0">', unsafe_allow_html=True)
    st.markdown('<div class="row-label" style="margin-bottom:8px">QUEUE</div>', unsafe_allow_html=True)

    if st.session_state.video_files:
        for vf in st.session_state.video_files[:5]:
            st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#555;margin-bottom:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">→ {vf.name}</div>', unsafe_allow_html=True)
        if len(st.session_state.video_files) > 5:
            st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#444">... +{len(st.session_state.video_files)-5} more</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#333">Empty queue</div>', unsafe_allow_html=True)

    if st.button("CLEAR ALL", key="btn_clear"):
        for k in ["video_files", "logo_file", "music_file", "video_folder", "music_folder", "output_folder", "log_lines"]:
            if k in ["video_files", "log_lines"]:
                st.session_state[k] = []
            elif k == "logo_file" or k == "music_file":
                st.session_state[k] = None
            else:
                st.session_state[k] = ""
        st.rerun()


# ─── Render Logic ─────────────────────────────────────────────────────────────
if render_clicked:
    errors = []
    if not (st.session_state.video_files or st.session_state.video_folder):
        errors.append("Chưa chọn video đầu vào")
    if not st.session_state.output_folder:
        errors.append("Chưa chọn thư mục output")
    if not check_ffmpeg():
        errors.append("FFmpeg chưa được cài đặt")
    if st.session_state.music_mode == "Thay nhạc" and not (st.session_state.music_file or st.session_state.music_folder):
        errors.append("Chế độ 'Thay nhạc' nhưng chưa chọn file nhạc")

    if errors:
        for e in errors:
            st.markdown(f'<div class="status-box error">✗ {e}</div>', unsafe_allow_html=True)
    else:
        st.session_state.log_lines = []
        add_log("═══════════════════════════════════", "info")
        add_log("  RENDER SESSION STARTED", "ok")
        add_log("═══════════════════════════════════", "info")

        os.makedirs(st.session_state.output_folder, exist_ok=True)
        add_log(f"  OUTPUT → {st.session_state.output_folder}", "info")

        videos_to_process = []

        # Collect videos
        if st.session_state.video_files:
            for vf in st.session_state.video_files:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=Path(vf.name).suffix)
                tmp.write(vf.read())
                tmp.close()
                videos_to_process.append((tmp.name, vf.name))
        elif st.session_state.video_folder and os.path.isdir(st.session_state.video_folder):
            exts = {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"}
            for f in sorted(Path(st.session_state.video_folder).iterdir()):
                if f.suffix.lower() in exts:
                    videos_to_process.append((str(f), f.name))

        add_log(f"  VIDEOS FOUND: {len(videos_to_process)}", "info")

        # Save logo to temp
        logo_tmp = None
        if st.session_state.logo_file:
            lt = tempfile.NamedTemporaryFile(delete=False, suffix=Path(st.session_state.logo_file.name).suffix)
            lt.write(st.session_state.logo_file.read())
            lt.close()
            logo_tmp = lt.name
            add_log(f"  LOGO → {st.session_state.logo_file.name} ({st.session_state.logo_mode})", "info")

        # Save music to temp
        music_tmp = None
        if st.session_state.music_file and st.session_state.music_mode == "Thay nhạc":
            mt = tempfile.NamedTemporaryFile(delete=False, suffix=Path(st.session_state.music_file.name).suffix)
            mt.write(st.session_state.music_file.read())
            mt.close()
            music_tmp = mt.name
            add_log(f"  MUSIC → {st.session_state.music_file.name}", "info")
        elif st.session_state.music_folder and st.session_state.music_mode == "Thay nhạc":
            music_files_found = []
            if os.path.isdir(st.session_state.music_folder):
                for f in sorted(Path(st.session_state.music_folder).iterdir()):
                    if f.suffix.lower() in {".mp3", ".wav", ".aac", ".flac", ".m4a"}:
                        music_files_found.append(str(f))
            if music_files_found:
                music_tmp = music_files_found[0]

        add_log("═══════════════════════════════════", "info")

        # Codec mapping
        codec_map = {
            "libx264 (H.264)": "libx264",
            "libx265 (H.265)": "libx265",
            "copy (giữ nguyên)": "copy",
        }
        crf_map = {
            "Cao (CRF 18)": 18,
            "Trung bình (CRF 23)": 23,
            "Thấp (CRF 28)": 28,
        }
        pos_map = {
            "Góc trên trái": "10:10",
            "Góc trên phải": "main_w-overlay_w-10:10",
            "Góc dưới trái": "10:main_h-overlay_h-10",
            "Góc dưới phải": "main_w-overlay_w-10:main_h-overlay_h-10",
            "Giữa": "(main_w-overlay_w)/2:(main_h-overlay_h)/2",
        }

        codec = codec_map.get(st.session_state.get("video_codec", "libx264 (H.264)"), "libx264")
        crf = crf_map.get(st.session_state.get("video_quality", "Trung bình (CRF 23)"), 23)
        logo_pos = pos_map.get(st.session_state.get("logo_position", "Góc trên trái"), "10:10")
        logo_scale_pct = st.session_state.get("logo_scale", 15)
        audio_vol = st.session_state.get("audio_volume", 100) / 100
        orig_vol = st.session_state.get("orig_volume", 100) / 100

        progress_bar = st.progress(0)
        total = len(videos_to_process)
        status_ph = st.empty()

        for idx, (src_path, orig_name) in enumerate(videos_to_process):
            stem = Path(orig_name).stem
            out_path = os.path.join(st.session_state.output_folder, f"{stem}_rendered.mp4")
            add_log(f"  [{idx+1}/{total}] {orig_name}", "info")
            status_ph.markdown(f'<div class="status-box">⚙ Processing: {orig_name} ({idx+1}/{total})</div>', unsafe_allow_html=True)

            # Build ffmpeg command
            inputs = ["-i", src_path]
            filter_complex_parts = []
            last_v = "[0:v]"
            last_a = "[0:a]" if st.session_state.music_mode == "Giữ nhạc gốc" else None

            if logo_tmp:
                inputs += ["-i", logo_tmp]
                logo_idx = 1
                scale_expr = f"iw*{logo_scale_pct}/100:-1"

                if st.session_state.logo_mode == "Đứng yên góc":
                    filter_complex_parts.append(
                        f"[{logo_idx}:v]scale={scale_expr}[logo];"
                        f"{last_v}[logo]overlay={logo_pos}[vout]"
                    )
                    last_v = "[vout]"
                else:  # Chạy viền trên
                    filter_complex_parts.append(
                        f"[{logo_idx}:v]scale={scale_expr}[logo];"
                        f"{last_v}[logo]overlay='if(gte(t,0),-overlay_w+t*100,NaN)':10[vout]"
                    )
                    last_v = "[vout]"

            if music_tmp and st.session_state.music_mode == "Thay nhạc":
                inputs += ["-i", music_tmp]
                music_input_idx = inputs.count("-i") - 1
                filter_complex_parts.append(
                    f"[0:a]volume={orig_vol}[a0];"
                    f"[{music_input_idx}:a]volume={audio_vol}[a1];"
                    "[a0][a1]amix=inputs=2:duration=first[aout]"
                )
                last_a = "[aout]"
            elif st.session_state.music_mode == "Giữ nhạc gốc" and orig_vol != 1.0:
                filter_complex_parts.append(f"[0:a]volume={orig_vol}[aout]")
                last_a = "[aout]"

            cmd = ["ffmpeg", "-y"] + inputs
            if filter_complex_parts:
                fc = ";".join(filter_complex_parts)
                cmd += ["-filter_complex", fc, "-map", last_v]
                if last_a:
                    cmd += ["-map", last_a]
            else:
                cmd += ["-map", "0:v"]
                if last_a:
                    cmd += ["-map", "0:a"]

            if codec != "copy":
                cmd += ["-c:v", codec, "-crf", str(crf), "-preset", "fast"]
            else:
                cmd += ["-c:v", "copy"]

            cmd += ["-c:a", "aac", "-b:a", "192k", out_path]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
                if result.returncode == 0:
                    size = format_size(out_path)
                    add_log(f"  ✓ Done → {Path(out_path).name} ({size})", "ok")
                else:
                    err_line = result.stderr.split("\n")[-3] if result.stderr else "Unknown error"
                    add_log(f"  ✗ Error: {err_line}", "err")
            except subprocess.TimeoutExpired:
                add_log(f"  ✗ Timeout: {orig_name}", "err")
            except Exception as e:
                add_log(f"  ✗ Exception: {str(e)}", "err")

            # Cleanup temp
            if src_path != orig_name and os.path.exists(src_path):
                try:
                    os.unlink(src_path)
                except:
                    pass

            progress_bar.progress((idx + 1) / total)

        # Cleanup logo/music temp
        for tmp_f in [logo_tmp, music_tmp]:
            if tmp_f and tmp_f.startswith(tempfile.gettempdir()) and os.path.exists(tmp_f):
                try:
                    os.unlink(tmp_f)
                except:
                    pass

        add_log("═══════════════════════════════════", "info")
        add_log("  ALL DONE", "ok")
        add_log("═══════════════════════════════════", "info")
        status_ph.markdown('<div class="status-box">✓ Render hoàn tất!</div>', unsafe_allow_html=True)
        st.rerun()
