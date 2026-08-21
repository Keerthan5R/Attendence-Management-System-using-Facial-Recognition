<div align="center">

# 🎓 Attendance Management System
### using Facial Recognition

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![TechSaksham](https://img.shields.io/badge/TechSaksham-Microsoft%20%26%20SAP-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://techsaksham.org)

**A real-time attendance tracking system powered by OpenCV's LBPH Face Recognizer.**  
Built as an internship project under **TechSaksham** — a joint CSR initiative by **Microsoft India & SAP India**, implemented by **Edunet Foundation**.

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 📷 **Face Registration** | Capture 100 face samples per student via webcam |
| 🧠 **LBPH Model Training** | Train OpenCV LBPH recognizer on registered students |
| 🎯 **Auto Attendance** | Real-time facial recognition marks attendance instantly |
| ✏️ **Manual Attendance** | Fill attendance manually when camera is unavailable |
| 📊 **Excel Export** | Styled `.xlsx` reports with student name, date, time, subject |
| 📧 **Email Notifications** | Auto-send HTML email alert when a student is marked present |
| 🌐 **Web Dashboard** | Flask-based browser UI to view, search & download records |
| 🔒 **Secure Config** | Credentials stored in `.env` — never hardcoded |

---

## 🖼️ Screenshots

> *Tkinter desktop app (left) · Flask web dashboard (right)*

<!-- Add your screenshots here after running the app -->
| Desktop App | Web Dashboard |
|---|---|
| ![Desktop](docs/screenshots/desktop.png) | ![Dashboard](docs/screenshots/dashboard.png) |

---

## 🗂️ Project Structure

```
📁 Attendance-Management-System-using-Facial-Recognition/
│
├── 📄 AMS_Run.py           # Main Tkinter desktop application
├── 📄 training.py          # Standalone model training script
├── 📄 testing.py           # Live face recognition test
├── 📄 app.py               # Flask web dashboard
├── 📄 notifier.py          # Email notification module
│
├── 📄 requirements.txt     # Python dependencies
├── 📄 .env.example         # Environment variable template
├── 📄 .gitignore
│
├── 📁 TrainingImage/       # Captured face images (auto-created, gitignored)
├── 📁 TrainingImageLabel/  # Trained model .yml (auto-created, gitignored)
├── 📁 Attendance/          # Excel attendance records (auto-created)
├── 📁 StudentDetails/      # Student CSV registry (auto-created)
│
├── 📄 haarcascade_frontalface_default.xml
└── 📄 haarcascade_frontalface_alt.xml
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.8+ |
| **Face Detection** | OpenCV Haar Cascade |
| **Face Recognition** | OpenCV LBPH (Local Binary Patterns Histogram) |
| **GUI** | Tkinter |
| **Web Dashboard** | Flask |
| **Data Export** | openpyxl (Excel), pandas |
| **Notifications** | smtplib (SMTP / Gmail) |
| **Config Management** | python-dotenv |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Keerthan5R/Attendence-Management-System-using-Facial-Recognition.git
cd Attendence-Management-System-using-Facial-Recognition
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Email (Optional)
```bash
cp .env.example .env
# Edit .env with your Gmail App Password
```

> **Tip**: To get a Gmail App Password:  
> Google Account → Security → 2-Step Verification → App Passwords

---

## 🎮 Usage

### Desktop Application (Tkinter)
```bash
python AMS_Run.py
```

**Workflow:**
1. **Register Student** → Captures 100 face images
2. **Train Model** → Trains LBPH recognizer (~30 seconds)
3. **Auto Attendance** → Enter subject name → face recognition runs live
4. **View Records** → Browse Excel files in-app

### Web Dashboard (Flask)
```bash
python app.py
# Open http://localhost:5000
```

### Train Model (Standalone)
```bash
python training.py
```

### Test Recognition (Standalone)
```bash
python testing.py
```

---

## 🔧 How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM PIPELINE                              │
│                                                                 │
│  1. CAPTURE    Webcam ──► Haar Cascade ──► 100 face images/student │
│                                                                 │
│  2. TRAIN      Images ──► LBPH Recognizer ──► trainer.yml      │
│                                                                 │
│  3. RECOGNIZE  Live webcam ──► Detect face ──► Predict ID      │
│                     └──► Confidence < 70 ──► Mark Present      │
│                     └──► Confidence ≥ 70 ──► Label Unknown     │
│                                                                 │
│  4. RECORD     pandas DataFrame ──► styled Excel .xlsx         │
│                                  ──► Email notification        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Confidence Threshold

The LBPH recognizer outputs a **confidence score** (lower = more confident):

| Confidence | Meaning |
|---|---|
| `< 70` | ✅ Recognized — mark attendance |
| `≥ 70` | ❌ Unknown — do not mark |

Adjust the threshold in `AMS_Run.py` → `auto_attendance()` function.

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `No module named cv2.face` | Install `opencv-contrib-python` not `opencv-python` |
| Camera not opening | Check `cv2.VideoCapture(0)` index; try `1` for external webcam |
| Model not found | Run `python training.py` before using Auto Attendance |
| Email not sending | Check `.env` credentials; ensure Gmail App Password is used |

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **TechSaksham** — *AI: Transformative Learning* internship program
- **Microsoft India & SAP India** — Joint CSR initiative sponsors
- **Edunet Foundation** — Implementation partner
- **OpenCV** — Open source computer vision library

---

<div align="center">

Made with ❤️ by **Keerthan R**  
*Gopalan College of Engineering and Management*  
*Visvesvaraya Technological University*

</div>
