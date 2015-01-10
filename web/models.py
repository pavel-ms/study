from django.db import models


class Car(models.Model):
    external_id = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    cover = models.CharField(max_length=255)
    price = models.IntegerField()
    descr = models.TextField()
