import os
import cv2
import numpy as np
from google.cloud import vision

# Set up Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\91964\OneDrive\Desktop\PAD_Rishi\exsel-452618-1eff91091801.json"

# Define necessary formal clothing items
REQUIRED_FORMAL_ITEMS = [
    {"shirt", "pants"},  # Men (Shirt + Pants)
    {"shirt", "trousers"},  # Alternative for men
    {"blouse", "skirt", "shawl"},  # Women (Blouse + Skirt + Shawl)
    {"shirt", "skirt", "shawl"},  # Women (Shirt + Skirt + Shawl)
    {"blouse", "pants", "shawl"},  # Women (Blouse + Pants + Shawl)
    {"shirt", "pants", "shawl"},  # Women (Shirt + Pants + Shawl)
    {"blouse", "skirt", "dupatta"},  # Women (Blouse + Skirt + Dupatta)
    {"shirt", "skirt", "dupatta"},  # Women (Shirt + Skirt + Dupatta)
    {"blouse", "pants", "dupatta"},  # Women (Blouse + Pants + Dupatta)
    {"shirt", "pants", "dupatta"},  # Women (Shirt + Pants + Dupatta)
    {"coat", "tie", "pants"},  # Business formal
    {"shirt"},  # Allow at least a shirt
    {"dupatta"},
    {"shawl"},
]

def detect_objects_google_vision(image):
    """Detects objects and labels in an image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.jpg', image)
    if not success:
        return set(), []

    image_data = encoded_image.tobytes()
    image = vision.Image(content=image_data)

    # Object detection
    response = client.object_localization(image=image)
    detected_objects = {obj.name.lower() for obj in response.localized_object_annotations}
    bounding_boxes = [(obj.name.lower(), [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices])
                      for obj in response.localized_object_annotations]

    print("Detected clothing:", detected_objects)  # Debugging detected objects

    return detected_objects, bounding_boxes

def is_formal_wear(detected_objects):
    """Checks if detected clothing matches any formal wear set."""
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

def main():
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        detected_objects, bounding_boxes = detect_objects_google_vision(frame)
        draw_boxes(frame, bounding_boxes)

        # Determine if any person is in formal attire
        if is_formal_wear(detected_objects):
            text = "FORMAL"
            color = (0, 255, 0)  # Green
        else:
            text = "NOT FORMAL"
            color = (0, 0, 255)  # Red

        # Display status
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.imshow("Formal Dress Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
