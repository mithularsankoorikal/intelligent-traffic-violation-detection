from django.shortcuts import render
import os
import cv2
from ultralytics import YOLO
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
from .models import *
from collections import Counter


# Create your views here.
# MODEL_PATH = os.path.join(settings.BASE_DIR, r"C:\Users\mithula\Desktop\Traffic Monitoring\CampusViolation\model\best1.pt")
# model = YOLO(MODEL_PATH)
MODEL_PATH = os.path.join(settings.BASE_DIR, "model", "best1.pt")
model = YOLO(MODEL_PATH)


def process_video(input_video_path, output_video_path):
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    violations_folder = os.path.join(settings.MEDIA_ROOT, "violations")
    os.makedirs(violations_folder, exist_ok=True)
    cap = cv2.VideoCapture(input_video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Run YOLO on the frame
        results = model(frame)
        detected_classes = set()  # Store detected class IDs in the current frame
        # Get detections
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])  # Get class ID
                confidence = float(box.conf[0])  # Get confidence score
                if confidence > 0.5:
                    detected_classes.add(cls_id)  # Store detected class
        # If both cls_id 1 and cls_id 3 are detected in the same frame
        if 1 in detected_classes and 3 in detected_classes:
            violation_img_path = os.path.join(violations_folder, f"violation_{frame_count}.jpg")
            cv2.imwrite(violation_img_path, frame)  # Save frame as an image
            # Save to database
            ViolationImage.objects.create(image_path=f"violations/violation_{frame_count}.jpg")
        # Count occurrences of each detected class
        class_counts = Counter(detected_classes)
        # Check if there are at least 3 helmets (0) and 1 number plates (3)
        if class_counts.get(0, 0) >= 3 and class_counts.get(3, 0) == 1:
            violation_img_path = os.path.join(violations_folder, f"violation_{frame_count}.jpg")
            cv2.imwrite(violation_img_path, frame)  # Save frame as an image
            # Save to database
            ViolationImage.objects.create(image_path=f"violations/violation_{frame_count}.jpg")
        # Get the processed frame with predictions
        output_frame = results[0].plot()
        # Write the frame to output video
        out.write(output_frame)
        frame_count += 1
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def home(request):
    processed_video_url = None
    if request.method == "POST" and request.FILES.get("video"):
        video = request.FILES["video"]
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        input_video_full_path = os.path.join(settings.MEDIA_ROOT, filename)
        output_video_name = "output_" + filename
        output_video_path = os.path.join(settings.MEDIA_ROOT, output_video_name)
        converted_video_name = "converted_" + filename
        converted_video_path = os.path.join(settings.MEDIA_ROOT, converted_video_name)
        process_video(input_video_full_path, output_video_path)
        if os.path.exists(output_video_path):
            ffmpeg_command = [
                "ffmpeg", "-i", output_video_path, "-vcodec", "h264", "-acodec", "aac",
                "-strict", "experimental", converted_video_path, "-y"
            ]
            subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if os.path.exists(converted_video_path):
                processed_video_url = settings.MEDIA_URL + converted_video_name
            else:
                processed_video_url = settings.MEDIA_URL + output_video_name
            # Save processed video info in the database
            ProcessedVideo.objects.create(video_name=filename, processed_video_url=processed_video_url)
    return render(request, "home.html", {"processed_video": processed_video_url})
