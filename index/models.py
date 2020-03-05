from django.db import models

# Create your models here.


class Banner(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    status = models.BooleanField()
    pic = models.ImageField(upload_to='imgs')
    path = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)
