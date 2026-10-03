import cv2
import serial
import time

# =========================
# 1. ESP32 CONNECTION
# =========================

esp32 = serial.Serial("COM7", 115200, timeout=0.1)

time.sleep(2)

print("✅ ESP32 connected")


# =========================
# 2. PHONE CAMERA
# =========================

PHONE_STREAM_URL = "http://10.119.179.63:8080/video"

camera = cv2.VideoCapture(PHONE_STREAM_URL)

if not camera.isOpened():
    print("❌ Could not connect to phone camera")
    esp32.close()
    exit()

print("✅ Phone camera connected")


# =========================
# 3. VARIABLES
# =========================

direction = None
ambulance_ready = False

frozen_frame = None


print()
print("===================================")
print(" SMART AMBULANCE SYSTEM")
print("===================================")
print("System ready")
print("Press A → Ambulance ready")
print("Press Q → Exit")
print("-----------------------------------")


# =========================
# 4. MAIN LOOP
# =========================

while True:

    # =========================
    # READ ESP32 DIRECTION
    # =========================

    data = esp32.readline().decode(errors="ignore").strip()

    if data:

        print("ESP32:", data)

        if "DIRECTION : NORTH" in data:
            direction = "NORTH"

            print("📍 Direction detected: NORTH")

        elif "DIRECTION : SOUTH" in data:
            direction = "SOUTH"

            print("📍 Direction detected: SOUTH")

        elif "DIRECTION : EAST" in data:
            direction = "EAST"

            print("📍 Direction detected: EAST")

        elif "DIRECTION : WEST" in data:
            direction = "WEST"

            print("📍 Direction detected: WEST")


    # =========================
    # CAMERA
    # =========================

    if not ambulance_ready:

        ret, frame = camera.read()

        if not ret:
            print("❌ Camera frame not received")
            break

        display_frame = frame

    else:

        display_frame = frozen_frame


    # =========================
    # SHOW CAMERA
    # =========================

    cv2.imshow("Smart Ambulance", display_frame)


    # =========================
    # KEYBOARD
    # =========================

    key = cv2.waitKey(1) & 0xFF


    # =========================
    # A → AMBULANCE READY
    # =========================

    if key == ord('a'):

        if not ambulance_ready:

            frozen_frame = frame.copy()

            cv2.imwrite(
                "ambulance_capture.jpg",
                frozen_frame
            )

            ambulance_ready = True

            print()
            print("===================================")
            print("🚑 AMBULANCE READY")
            print("📸 Ambulance position captured")
            print("===================================")


    # =========================
    # Q → EXIT
    # =========================

    elif key == ord('q'):

        print("Closing system...")
        break


# =========================
# 5. CLOSE EVERYTHING
# =========================

camera.release()
cv2.destroyAllWindows()

esp32.close()

print("System closed")