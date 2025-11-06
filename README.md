# cv.py

🍎🍌🍊 Fruit and Ripeness Detection using OpenCV

This project uses **Computer Vision** techniques with **OpenCV** and **NumPy** to automatically detect fruits (Apple, Banana, and Orange) from a webcam feed and determine their **ripeness level** based on color analysis.

---

## 🚀 Features
- Real-time fruit detection using a webcam  
- Identifies **Apple**, **Banana**, and **Orange**  
- Determines **ripeness** level:
  - 🍌 **Banana:** Green → Yellow → Brown  
  - 🍎 **Apple:** Unripe → Ripe → Over-ripe  
  - 🍊 **Orange:** Unripe → Ripe → Over-ripe  
- Displays bounding box, fruit name, and ripeness status on the video feed  

---

## 🧠 How It Works
1. Captures video frames from your webcam using `cv2.VideoCapture()`.
2. Converts the frame from **BGR to HSV** color space.
3. Uses **color thresholding** (`cv2.inRange()`) to isolate fruit regions.
4. Finds **contours** (`cv2.findContours()`) to locate the fruit.
5. Calculates the **average hue** inside the detected fruit region to determine ripeness.
6. Displays the fruit name and ripeness status on the live video.

---
