from django.db import models
from django.conf import settings


class Doubt(models.Model):
    question = models.CharField(max_length=255)
    question_type = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
