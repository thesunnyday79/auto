# 🎬 Auto Render Video – Full Length

Tool tự động render video hàng loạt với logo và nhạc nền, xây dựng bằng Python + Streamlit + FFmpeg.

---

## ✅ Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| **Video** | Chọn file đơn lẻ hoặc cả folder |
| **Logo** | Chèn logo tĩnh (góc) hoặc chạy viền trên |
| **Music** | Giữ nhạc gốc hoặc thay bằng nhạc nền mới |
| **Output** | Chỉ định thư mục lưu file đã render |
| **Options** | Vị trí logo, kích thước, codec, CRF, volume |
| **Log** | Hiển thị log từng bước ngay trong giao diện |

---

## 🚀 Cài đặt & Chạy Local

### 1. Clone repo

```bash
git clone https://github.com/YOUR_USERNAME/auto-render-video.git
cd auto-render-video
```

### 2. Cài FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg -y
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Tải từ https://ffmpeg.org/download.html và thêm vào PATH.

### 3. Cài Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy app

```bash
streamlit run app.py
```

---

## ☁️ Deploy lên Streamlit Cloud

1. Push code lên GitHub (public hoặc private repo)
2. Vào https://share.streamlit.io → **New app**
3. Chọn repo → branch → file `app.py`
4. Click **Deploy**

> ⚠️ **Lưu ý khi deploy cloud:** Streamlit Cloud không có FFmpeg mặc định.  
> Cần tạo file `.streamlit/packages.txt` với nội dung:
> ```
> ffmpeg
> ```

---

## 📁 Cấu trúc file

```
auto-render-video/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── packages.txt          # System packages (FFmpeg cho cloud)
└── README.md
```

---

## ⚙️ Options

| Option | Mô tả |
|--------|-------|
| Vị trí logo | Góc trên/dưới trái/phải, giữa |
| Kích thước logo | 5–30% chiều rộng video |
| Video Codec | H.264, H.265, hoặc copy |
| Chất lượng (CRF) | Cao (18), Trung bình (23), Thấp (28) |
| Âm lượng nhạc nền | 0–200% |
| Âm lượng nhạc gốc | 0–200% |

---

## 📝 License

MIT License
