import os
import cv2
import numpy as np
import threading
import time
from datetime import datetime
from ultralytics import YOLO
from google.cloud import vision

# ✅ Initialize Google Vision API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\91964\OneDrive\Desktop\PAD_Rishi\exsel-452618-1eff91091801.json"
vision_client = vision.ImageAnnotatorClient()

# ✅ Load YOLO model for ID card detection
yolo_model = YOLO(r"C:\Users\91964\OneDrive\Desktop\PAD_Rishi\runs\detect\train3\weights\best.pt")

# ✅ Define required formal clothing items
REQUIRED_FORMAL_ITEMS = [
    {"shirt", "pants"}, {"shirt", "trousers"}, {"blouse", "skirt", "dupatta"},
    {"shirt", "skirt", "dupatta"}, {"blouse", "pants", "dupatta"}, {"shirt", "pants", "dupatta"},
    {"coat", "tie", "pants"}, {"suit", "tie"}, {"blazer", "tie", "pants"},
    {"kurta", "pajama"}, {"formal dress"}, {"saree"}, {"blazer", "shirt", "trousers"},
    {"three-piece suit"}, {"dupatta", "blouse", "skirt"}, {"dupatta", "shirt", "pants"},
    {"top", "pants"}, {"top", "trousers"}, {"top", "skirt"}, {"clothing"},
    {"top"}, {"shirt"}  # Ensure "top" and "shirt" alone are considered formal
]

# ✅ Automatically create violation folders
base_folder = os.path.join(os.getcwd(), "Violations")  # Saves in script directory
no_id_folder = os.path.join(base_folder, "No_ID_Card")
no_formal_folder = os.path.join(base_folder, "No_Formal_Dress")

os.makedirs(no_id_folder, exist_ok=True)
os.makedirs(no_formal_folder, exist_ok=True)

# ✅ Track last save time to ensure images are saved every 5 seconds
last_save_time = time.time()

def detect_objects_google_vision(image):
    """Detects objects in an image using Google Cloud Vision API."""
    success, encoded_image = cv2.imencode('.jpg', image)
    if not success:
        return set(), []

    image_data = encoded_image.tobytes()
    image = vision.Image(content=image_data)

    response = vision_client.object_localization(image=image)
    detected_objects = {obj.name.lower() for obj in response.localized_object_annotations}
    bounding_boxes = [(obj.name.lower(), [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices])
                      for obj in response.localized_object_annotations]

    return detected_objects, bounding_boxes

def is_formal_wear(detected_objects):
    """Checks if detected clothing meets formal wear criteria."""
    for formal_set in REQUIRED_FORMAL_ITEMS:
        if formal_set.issubset(detected_objects):
            return True
    return False

def draw_boxes(image, bounding_boxes):
    """Draws bounding boxes around detected clothing items."""
    h, w, _ = image.shape

    for obj_name, box in bounding_boxes:
        pts = np.array([[int(x * w), int(y * h)] for x, y in box], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(image, obj_name, (pts[0][0][0], pts[0][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# ✅ Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

def process_frame():
    global last_save_time
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not capture frame")
            break

        # ✅ Copy frames for parallel processing
        yolo_frame = frame.copy()
        vision_frame = frame.copy()

        # ✅ Run YOLO for ID card detection
        yolo_results = yolo_model(yolo_frame)
        detected_classes = [yolo_model.names[int(box.cls)] for result in yolo_results for box in result.boxes]

        # ✅ Check if "id_card" is detected
        id_card_detected = "id_card" in detected_classes

        # ✅ Run Google Vision in a separate thread for efficiency
        vision_thread = threading.Thread(target=lambda: detect_objects_google_vision(vision_frame))
        vision_thread.start()
        detected_objects, bounding_boxes = detect_objects_google_vision(vision_frame)
        vision_thread.join()

        # ✅ Determine if formal wear is detected
        formal_detected = is_formal_wear(detected_objects)

        # ✅ Display ID card detection window
        for result in yolo_results:
            img = result.plot()
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.putText(img_bgr, f"ID Card: {'Detected' if id_card_detected else 'Not Detected'}",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if id_card_detected else (0, 0, 255), 3)
            cv2.imshow("YOLO ID Card Detection", img_bgr)

        # ✅ Display formal dress detection window
        draw_boxes(vision_frame, bounding_boxes)
        cv2.putText(vision_frame, f"Formal Wear: {'Yes' if formal_detected else 'No'}",
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if formal_detected else (0, 0, 255), 3)
        cv2.imshow("Google Vision Formal Dress Detection", vision_frame)

        # ✅ Save images based on violation type (every 5 seconds)
        current_time = time.time()
        if current_time - last_save_time >= 5:
            last_save_time = current_time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if not id_card_detected:
                no_id_path = os.path.join(no_id_folder, f"No_ID_{timestamp}.jpg")
                cv2.imwrite(no_id_path, frame)
                print(f"🚨 No ID Card detected! Image saved at: {no_id_path}")

            if not formal_detected:
                no_formal_path = os.path.join(no_formal_folder, f"No_Formal_{timestamp}.jpg")
                cv2.imwrite(no_formal_path, frame)
                print(f"🚨 No Formal Dress detected! Image saved at: {no_formal_path}")

        # ✅ Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_frame()
