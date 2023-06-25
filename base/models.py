from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SchoolInfo(models.Model):
    school=models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.school
    
class SemesterInfo(models.Model):
    year=models.CharField(max_length=10,
                            choices=[("2023", "2023")],
                            default="2023")
    semester=models.CharField(max_length=50,
                            choices=[("1학기", "1학기"), ("2학기", "2학기")],
                            default="1학기")

    def __str__(self):
        return self.year+" "+self.semester

class student_enrolled(models.Model):
    school=models.ForeignKey(SchoolInfo, on_delete=models.CASCADE, related_name='student_list')
    semester=models.ForeignKey(SemesterInfo, on_delete=models.CASCADE, related_name='student_list')
    not_enrolled=models.CharField(max_length=100, blank=True)

class UserInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE, related_name='UserInfo')
    semester=models.ForeignKey(SemesterInfo, on_delete=models.CASCADE, related_name='UserInfo', default=1)

