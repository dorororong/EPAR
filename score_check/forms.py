from django import forms
from .models import ReferenceScore, ReferenceSubsubject, Reference_Grade_Subject
from base.models import UserInfo
from django.contrib.auth.models import User

class UploadFileForm(forms.Form):
    file = forms.FileField()
#
# class ReferenceScoreForm(forms.Form):
#     subsubject_id= forms.CharField(max_length=50)
#     score_name = forms.CharField(max_length=50)
#     score_list = forms.CharField(max_length=200)


class ReferenceScoreForm(forms.ModelForm):
    class Meta:
        model = ReferenceScore
        fields = ['subsubject', 'score_name', 'score_list']
        # put labels here
        labels = {
            'subsubject': '과목',
            'score_name': '세부점수명 :',
            'score_list': '점수표 :',
        }
        widgets = {
            'score_list': forms.TextInput(attrs={'size': '40'}),
        }


GRADE_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
]

class subject_subsubject_Form(forms.ModelForm):
    subsubject = forms.CharField(max_length=10)
    grade = forms.ChoiceField(choices=GRADE_CHOICES)
    class Meta:
        model = Reference_Grade_Subject
        fields = ['grade', 'subject']


    def save(self, commit=True):

        user = User.objects.get(username=self.request.user)
        userinfo = UserInfo.objects.get(user=user)
        instance, created = Reference_Grade_Subject.objects.get_or_create(
            school=userinfo.school,
            semester=userinfo.semester,
            grade=self.cleaned_data['grade'],
            subject=self.cleaned_data['subject'],
        )

        subsubject = ReferenceSubsubject(
            subject=instance,
            subsubject=self.cleaned_data['subsubject']
        )
        subsubject.save()  # Save the ReferenceSubsubject instance

        return instance  # Add this line

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(subject_subsubject_Form, self).__init__(*args, **kwargs)




