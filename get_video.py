import cv2

# đường dẫn video gốc và video xuất
input_path = "src/video_demo/test_video.mp4"
output_path = "src/video_demo/demo.mp4"

# mở video
cap = cv2.VideoCapture(input_path)

# lấy fps, kích thước khung hình
fps = 30  # đặt cố định 30fps như yêu cầu
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# tạo video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# tính frame bắt đầu và kết thúc
start_time = 20  # giây
end_time = 40
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)

# nhảy đến frame bắt đầu
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# đọc và ghi từng frame
current_frame = start_frame
while cap.isOpened() and current_frame < end_frame:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    current_frame += 1

# giải phóng tài nguyên
cap.release()
out.release()

print("đã tạo video mới từ giây 30 đến 40 tại:", output_path)
