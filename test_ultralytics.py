import sys

try:
    from ultralytics import YOLO
    print("SUCCESS: Ultralytics imported correctly")
    print("YOLO class available:", YOLO)
except ImportError as e:
    print("ERROR: Failed to import ultralytics")
    print("Error:", str(e))
    sys.exit(1)

try:
    # Test if we can load a model
    model = YOLO('yolov8n.pt')
    print("SUCCESS: YOLO model loaded correctly")
except Exception as e:
    print("WARNING: Could not load YOLO model (this is OK if you don't have the model yet)")
    print("Error:", str(e))

print("Ultralytics test completed")