from django.db import models
from base.models import SchoolInfo, SemesterInfo
# Create your models here.


class Reference_Grade_Subject(models.Model):
    school = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE, related_name='ReferenceSubject')
    semester = models.ForeignKey(SemesterInfo, on_delete=models.CASCADE, related_name='ReferenceSubject')
    grade = models.CharField(max_length=10)
    subject = models.CharField(max_length=10)

    def __str__(self):
        return self.grade + "-" + self.subject



class ReferenceSubsubject(models.Model):
    subject = models.ForeignKey(Reference_Grade_Subject, on_delete=models.CASCADE, related_name='ReferenceSubject')
    subsubject = models.CharField(max_length=10)
    def __str__(self):
        return self.subsubject

class ReferenceScore(models.Model):
    subsubject = models.ForeignKey(ReferenceSubsubject, on_delete=models.CASCADE, related_name='ReferenceSubsubject')
    score_name = models.CharField(max_length=50)
    score_list = models.CharField(max_length=200)

    def __str__(self):
        return self.subsubject.subsubject +"_" + self.score_name +' 점수표'
#
#
#
