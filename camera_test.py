import cv2
import sys

print("Testing camera access...")
print(f"OpenCV version: {cv2.__version__}")

# Test available cameras
for i in range(3):  # Test first 3 camera indices
    print(f"\n--- Testing camera index {i} ---")
    cap = cv2.VideoCapture(i)
    
    if not cap.isOpened():
        print(f"Camera {i}: Cannot open")
        continue
    
    # Get camera properties
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Camera {i}: Resolution {width}x{height}, FPS: {fps}")
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret:
        print(f"Camera {i}: Successfully captured frame")
        print(f"Frame shape: {frame.shape}")
        print(f"Frame dtype: {frame.dtype}")
        print(f"Frame min/max values: {frame.min()}/{frame.max()}")
        
        # Save test frame
        cv2.imwrite(f'test_frame_camera_{i}.jpg', frame)
        print(f"Test frame saved as 'test_frame_camera_{i}.jpg'")
    else:
        print(f"Camera {i}: Failed to capture frame")
    
    cap.release()

print("\n--- Testing with different backend APIs ---")
backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2]
backend_names = ["DirectShow", "Media Foundation", "Video4Linux2"]

for backend, name in zip(backends, backend_names):
    print(f"\nTesting {name} backend...")
    cap = cv2.VideoCapture(0, backend)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"{name}: Working - Frame shape: {frame.shape}")
        else:
            print(f"{name}: Opened but cannot read frame")
        cap.release()
    else:
        print(f"{name}: Cannot open camera")

print("\nCamera test completed. Check the test_frame_*.jpg files to see if frames were captured.")
