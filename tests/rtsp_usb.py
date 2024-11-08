# import rtsp
# with rtsp.Client(0) as client: # previews USB webcam 0
    # client.preview()
	
# 1/0
	
import cv2

def preview_usb_camera(camera_id=0, win_name="USB Camera Preview"):
    # 打开摄像头
    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}.")
        return

    while True:
        # 读取一帧
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # 显示帧
        cv2.imshow(win_name, frame)

        # 检查用户是否按下了 'q' 键来退出预览
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

# 预览 USB 摄像头 0
preview_usb_camera(camera_id=0)