from django import forms
from django.contrib.auth.models import User
from .models import UserInfo
from .models import SchoolInfo, SemesterInfo, student_enrolled


class School_infoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = ['school']
class Semester_infoForm(forms.ModelForm):
    class Meta:
        model = SemesterInfo
        fields = ['year', 'semester']



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserInfoForm(forms.Form):

    semester = forms.ModelChoiceField(queryset=SemesterInfo.objects.all(), empty_label="학기")
    school = forms.CharField(max_length=100, required=True)

class student_enrolledForm(forms.ModelForm):
    class Meta:
        model = student_enrolled
        fields = ['not_enrolled', 'school', 'semester']

