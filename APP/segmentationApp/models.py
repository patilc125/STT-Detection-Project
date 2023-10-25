from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/media/images')

# Create your models here.
class segmentationApp(models.Model):
    upload = models.ImageField(upload_to='images/')
    segmentation = models.ImageField(storage=fs)
    def __str__(self):
        return str(self.pk)

