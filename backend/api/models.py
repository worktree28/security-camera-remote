from django.db import models

# Create your models here.
class Snap(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    img_url = models.CharField(max_length=100, null=True)