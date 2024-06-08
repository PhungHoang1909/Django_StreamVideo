from django.db import models

class VideoGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VideoStream(models.Model):
    group = models.ForeignKey(VideoGroup, related_name='streams', on_delete=models.CASCADE)
    rtsp_url = models.URLField()

    def __str__(self):
        return self.rtsp_url
