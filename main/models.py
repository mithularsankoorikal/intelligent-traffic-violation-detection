from django.db import models

# Create your models here.


class ProcessedVideo(models.Model):
    video_name = models.CharField(max_length=255)
    processed_video_url = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ViolationImage(models.Model):
    image_path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_path
