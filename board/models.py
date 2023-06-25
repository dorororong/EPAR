from django.db import models

# Create your models here.



class Post(models.Model):
    postname=models.CharField(max_length=100)
    content=models.TextField()

    def __str__(self):
        return self.postname