import cv2
from ultralytics import YOLO

# For real testing, swap "yolov8n.pt" with "runs/detect/train/weights/best.pt" after training
model = YOLO("yolov8n.pt") 

# Target default webcam device
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam stream.")
    exit()

print("Press 'q' key to safely exit the live stream.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run inference stream on current frame
    results = model(frame, stream=True)

    # Annotate frame with boxes, labels, and confidence metrics
    for r in results:
        annotated_frame = r.plot()

    # Render frame in custom pop-up window
    cv2.imshow("VisionGuard - System Active", annotated_frame)

    # Clean kill loop upon pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()