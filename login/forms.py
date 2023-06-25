from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from base.models import UserInfo, SchoolInfo, SemesterInfo



class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    school = forms.CharField(required=True,
                             label='학교',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School'})
                             )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),  # Added this line
        }

        labels = {
            'username': '사용자 이름',
            'email': '이메일',
            'password1': '비밀번호(8자 이상, 특수문자 포함)',
            'password2': '비밀번호 확인',
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            school = self.cleaned_data['school']
            school_obj, created = SchoolInfo.objects.get_or_create(school=school)
            UserInfo.objects.create(user=user, school=school_obj)
        return user