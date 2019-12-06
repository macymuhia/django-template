from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=60, blank=False)
    description = models.TextField(
        max_length=300, blank=True, null=True, default='')

    @classmethod
    def get_all_departments(cls):
        return cls.objects.all()

    def __str__(self):
        return self.name
