import cv2
import numpy as np
import time

print("Advanced Camera Diagnostics")
print("=" * 40)

# Test all possible camera indices and backends
camera_indices = [0, 1, 2, 3]
backends = {
    'AUTO': cv2.CAP_ANY,
    'DSHOW': cv2.CAP_DSHOW,
    'MSMF': cv2.CAP_MSMF,
    'FFMPEG': cv2.CAP_FFMPEG
}

working_configs = []

for cam_idx in camera_indices:
    print(f"\n--- Testing Camera {cam_idx} ---")
    
    for backend_name, backend_code in backends.items():
        print(f"  Testing {backend_name} backend...")
        
        cap = cv2.VideoCapture(cam_idx, backend_code)
        
        if not cap.isOpened():
            print(f"    Failed to open")
            continue
            
        # Try to set some properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Try to read multiple frames
        success_count = 0
        for i in range(5):
            ret, frame = cap.read()
            if ret and frame is not None:
                success_count += 1
                
                # Check if frame is actually black
                if frame.mean() > 10:  # Not completely black
                    print(f"    SUCCESS: Frame captured, mean pixel value: {frame.mean():.1f}")
                    print(f"    Frame shape: {frame.shape}, dtype: {frame.dtype}")
                    
                    # Save a test frame
                    cv2.imwrite(f'test_cam{cam_idx}_{backend_name}.jpg', frame)
                    print(f"    Test frame saved: test_cam{cam_idx}_{backend_name}.jpg")
                    
                    working_configs.append((cam_idx, backend_name, backend_code))
                    break
                else:
                    print(f"    Frame captured but black (mean: {frame.mean():.1f})")
            else:
                print(f"    Failed to read frame {i+1}")
                time.sleep(0.1)
        
        cap.release()
        
        if success_count > 0:
            break  # Move to next camera if this backend works

print(f"\n{'='*40}")
print("SUMMARY:")
print(f"Working configurations found: {len(working_configs)}")

if working_configs:
    print("\nWorking camera configurations:")
    for cam_idx, backend_name, backend_code in working_configs:
        print(f"  Camera {cam_idx} with {backend_name} backend")
    
    # Use the first working configuration
    best_cam, best_backend_name, best_backend_code = working_configs[0]
    print(f"\nRecommended configuration: Camera {best_cam}, {best_backend_name}")
    
    # Create a simple test with the best configuration
    print(f"\nTesting recommended configuration...")
    cap = cv2.VideoCapture(best_cam, best_backend_code)
    
    if cap.isOpened():
        print("Camera opened successfully!")
        print("Press 'q' to quit the test window")
        
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Camera Test - Working Configuration', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Lost frame, trying to recover...")
                time.sleep(0.1)
        
        cap.release()
        cv2.destroyAllWindows()
else:
    print("\nNo working camera configurations found!")
    print("\nTroubleshooting suggestions:")
    print("1. Check if camera is connected and not used by another application")
    print("2. Try restarting the computer")
    print("3. Check camera drivers in Device Manager")
    print("4. Try a different USB port")
    print("5. Test camera with Windows Camera app first")
