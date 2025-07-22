# ID Card and Formal Dress Code Detection System

This project is a computer vision-based compliance monitoring system that detects ID card usage and verifies formal dress code adherence using a combination of YOLOv8 object detection and the Google Cloud Vision API. The system is integrated with automated email alerts and real-time violation logging for efficient monitoring.

## 🚀 Features

- 🎯 **Real-Time ID Card Detection** using YOLOv8 (trained custom model)
- 👔 **Formal Dress Code Verification** using Google Cloud Vision API
- 📸 **Violation Monitoring & Evidence Capture**
- 📧 **Automated Email Alerts** with zipped violation images
- 🌐 **React-Based Web Interface** for monitoring & visualization

---

## 📁 Project Structure

```
├── Id-card-1/                 # YOLO training dataset (train, test, valid)
├── Violations/                # Saved images of detected violations
│   ├── No_ID_Card/
│   └── No_Formal_Dress/
├── yolo/                      # Trained YOLO weights (best.pt)
├── main.py                   # Main app - integrates detection and processing
├── dress.py                  # Handles dress detection (Google Vision API)
├── send.py                   # Handles email alerts
└── README.md                 # Project Documentation
```

---

<img src="https://github.com/NARREDDYRISHITHA/ID-Card-and-Formal-Dress-Code-Detection-System/blob/7068f759ac6be2f2eefdcf6215c8a6106124cf0d/22S02-19Poster.png?raw=true" alt="Poster" width="400"/>


   **Fig.4 Formal Dress Code Compliance Monitoring Flow**

1. Live video feed is analyzed in real-time.
2. ID card is detected using YOLOv8
3. Dress type is detected via Google Vision API.
4. If any violation (No ID / No Formal Dress) is found:
   - Captures the image
   - Saves to the appropriate folder
   - Sends an automated alert email with a .zip attachment

---




**Fig.2 Formal and ID Card Detection**

- ✅ Detected ID Card and Formal Dress
- ❌ No ID Card but Formal Dress



![43efb79e-a942-400c-af18-696db55df643](https://github.com/user-attachments/assets/1d87efa8-6f31-49c6-8329-b0b6fe228983)
**Fig.3 Email Alert with Zipped Violations**

---

## 📦 Requirements

- Python 3.8+
- OpenCV
- YOLOv8 with Ultralytics
- Google Cloud Vision API (Credentials required)
- Flask
- smtplib (for email)

---
# ⚙️ Setup Instructions

## Clone the repository
```
git clone https://github.com/yourusername/formal-id-detection.git
cd formal-id-detection
```
## Install dependencies
```
pip install -r requirements.txt
-Add your Google Vision API credentials in dress.py
```
## Run the main script
```
python main.py
```

---

## 📫 Email Alert System
- Sends violation reports to the specified email ID.
- Emails include a `.zip` file containing images of non-compliant individuals.
- Example:

<img src="https://github.com/user-attachments/assets/729adcff-a75c-4073-bbcc-e7a5737f8fb6" alt="Reduced Height Image" height="400"/>

---

## 🛠️ Customization
- Change dress code logic in `dress.py`
- Update email list and SMTP settings in `send.py`
- Modify object detection threshold in `main.py`

---

## 📸 Model Training
- The YOLOv12 model was trained using custom dataset in `Id-card-1/`
- Use [Roboflow](https://roboflow.com/) or manual labeling tools for annotation
- Trained using `ultralytics` package:

```bash
yolo task=detect mode=train model=yolov12.yaml data=data.yaml epochs=100 imgsz=640
```




