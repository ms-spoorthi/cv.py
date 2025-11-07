import cv2
import numpy as np
import streamlit as st

st.title("🍎 Fruit Detection and Ripeness Classification")
st.markdown("Detects **Apple**, **Banana**, or **Orange** and determines their ripeness in real-time or from an uploaded image.")

# Sidebar
mode = st.sidebar.radio("Choose Input Mode:", ["📷 Webcam", "🖼️ Upload Image"])

# Detection function
def get_fruit_and_ripeness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ranges = {
        "Apple": (np.array([0, 120, 70]), np.array([10, 255, 255])),  # red apple
        "Banana": (np.array([20, 100, 100]), np.array([35, 255, 255])),  # yellow banana
        "Orange": (np.array([8, 150, 150]), np.array([20, 255, 255]))  # orange
    }

    fruit = "Unknown"
    status = ""

    for name, (lower, upper) in ranges.items():
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) > 2000:
                fruit = name
                x, y, w, h = cv2.boundingRect(cnt)
                roi = hsv[y:y + h, x:x + w]
                avg_hue = int(np.mean(roi[:, :, 0]))

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, fruit, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Ripeness logic
                if fruit == "Banana":
                    if avg_hue > 32:
                        status = "Unripe (Green)"
                    elif 20 < avg_hue <= 32:
                        status = "Ripe (Yellow)"
                    else:
                        status = "Over-ripe (Brown)"
                elif fruit == "Apple":
                    if avg_hue < 5:
                        status = "Ripe"
                    elif avg_hue < 15:
                        status = "Unripe"
                    else:
                        status = "Over-ripe"
                elif fruit == "Orange":
                    if avg_hue < 14:
                        status = "Ripe"
                    elif avg_hue < 20:
                        status = "Unripe"
                    else:
                        status = "Over-ripe"

                cv2.putText(frame, f"Status: {status}", (x, y + h + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                return frame

    return frame


# ---- Webcam Mode ----
if mode == "📷 Webcam":
    st.write("Press **Stop** to end webcam stream.")
    run = st.checkbox("Start Webcam")

    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        if not ret:
            st.write("Error accessing camera.")
            break
        frame = get_fruit_and_ripeness(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    cap.release()

# ---- Upload Image Mode ----
elif mode == "🖼️ Upload Image":
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)
        result = get_fruit_and_ripeness(frame)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        st.image(result, caption="Processed Image", use_column_width=True)
