import cv2
import numpy as np


def get_fruit_and_ripeness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Color ranges (HSV) - updated for better separation
    ranges = {
        "Apple": (np.array([0, 120, 70]), np.array([10, 255, 255])),  # red apple
        "Banana": (np.array([20, 100, 100]), np.array([35, 255, 255])),  # yellow banana range wider
        "Orange": (np.array([8, 150, 150]), np.array([20, 255, 255]))  # orange refined
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

                # ROI (Region of Interest)
                roi = hsv[y:y + h, x:x + w]
                avg_hue = int(np.mean(roi[:, :, 0]))  # Average hue inside fruit region

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, fruit, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

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


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = get_fruit_and_ripeness(frame)
    cv2.imshow("Fruit Detection + Ripeness", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
