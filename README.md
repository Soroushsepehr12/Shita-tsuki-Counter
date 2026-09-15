# 🥋 Shita Tsuki Counter Mediapipe

A real-time karate punch detection and counting system built with **Python, OpenCV, and MediaPipe Pose**.

Shita Tsuki Counter uses computer vision and human pose estimation to detect and count punches by analyzing body landmarks, wrist movement, elbow angles, and dynamic training zones.

This is **Version 1 (V1)** of the project. Future versions will introduce new detection features, improved architecture, and advanced martial arts training systems.

---

# 🎥 Demo Video

Click the image below to watch the Shita Tsuki Counter Mediapipe V1 demonstration:

[![Shita Tsuki Counter Demo](https://img.youtube.com/vi/DM-pAdnQciE/maxresdefault.jpg)](https://youtu.be/DM-pAdnQciE)
---

# ✨ Features

## 🥋 Shita Tsuki Detection

The system detects punches using:

- MediaPipe Pose landmarks
- Wrist tracking
- Elbow angle calculations
- Guard position detection
- Punch validation logic

---

## 🎯 Dynamic Training Zones

The system creates adaptive zones based on body proportions:

- Guard zone
- Punch zone
- Shoulder width calculation
- Hip and shoulder positioning

---

# 🧠 How It Works

1. Camera captures user movement
2. MediaPipe detects body landmarks
3. The program analyzes:
   - Wrist position
   - Elbow angle
   - Body position
   - Punch conditions
4. Valid punches are counted in real time

---

# 🧩 Technologies

- Python
- OpenCV
- MediaPipe
- NumPy

---

# 📁 Project Structure

```
Shita-Tsuki-Counter-Mediapipe/

├── shita_tsuki.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python shita_tsuki.py
```

---

# 📦 Requirements

```
opencv-python
mediapipe
numpy
```

---

# 🚀 Future Versions

## V2

Planned improvements:

- Knee strike detection
- Hit flash effects
- Sound effects
- Object-oriented refactor
- Improved tracking

## Future

- Multiple martial arts techniques
- Training statistics
- AI movement feedback
- Performance analysis

---

# 🎨 Development Philosophy

This project focuses on:

- Applying AI to real-world movement
- Learning computer vision
- Building interactive training tools
- Exploring human pose estimation

---

# 📜 License

MIT License
