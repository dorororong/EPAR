from django.db import models

# Create your models here.



class Post(models.Model):
    postname=models.CharField(max_length=100)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.CharField(max_length=100)

    def __str__(self):
        return self.postname