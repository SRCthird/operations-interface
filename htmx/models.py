from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Element(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        max_length=100
    )
    content = RichTextField()
    
    def __str__(self):
        return self.name
    
class Resource(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        max_length=100
    )
    photo = models.ImageField()
    url = models.URLField()