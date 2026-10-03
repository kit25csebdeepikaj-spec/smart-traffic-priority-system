import cv2

# Your phone IP Webcam URL
PHONE_STREAM_URL = "http://10.145.148.3:8080/video"

camera = cv2.VideoCapture(PHONE_STREAM_URL)

if not camera.isOpened():
    print("❌ Could not connect to phone camera")
    exit()

print("✅ Phone camera connected")
print("Press A → Freeze and capture ambulance position")
print("Press Q → Close camera")

ambulance_ready = False
frozen_frame = None

while True:

    # If ambulance is NOT ready, show live camera
    if not ambulance_ready:

        ret, frame = camera.read()

        if not ret:
            print("❌ Could not receive video from phone")
            break

        display_frame = frame

    else:
        # Ambulance ready → keep showing frozen image
        display_frame = frozen_frame

    cv2.imshow("Smart Ambulance - Camera", display_frame)

    key = cv2.waitKey(1) & 0xFF

    # -------------------------
    # A → Freeze current frame
    # -------------------------
    if key == ord('a'):

        if not ambulance_ready:

            # Save the current frame
            frozen_frame = frame.copy()

            # Save image
            cv2.imwrite("ambulance_capture.jpg", frozen_frame)

            # Send/set data in Python
            ambulance_ready = True

            print("🚑 Ambulance position captured!")
            print("ambulance_ready =", ambulance_ready)
            print("📸 Image saved as ambulance_capture.jpg")
            print("Camera is now FROZEN")

    # -------------------------
    # Q → Close camera
    # -------------------------
    elif key == ord('q'):

        print("Closing camera...")

        break


# Release camera
camera.release()

# Close OpenCV window
cv2.destroyAllWindows()

print("Camera closed")