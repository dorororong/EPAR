from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import UserInfoForm, UserForm, student_enrolledForm
from  django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import UserInfo, SchoolInfo, SemesterInfo, student_enrolled
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse


# Create your views here.
def main_view(request):
    username = request.user.username
    school = None
    try: school = request.user.userinfo.school
    except: pass
    return render(request, 'base/main.html', {'username': username, 'school': school})

class my_page_view(LoginRequiredMixin, View):
    template_name = 'base/my_page.html'
    success_url = reverse_lazy('base:main')

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)

        # Get the initial school name
        initial_school_name = request.user.userinfo.school.school
        initial_semester = request.user.userinfo.semester
        user_info_form = UserInfoForm(initial={'school': initial_school_name, 'semester': initial_semester })

        return render(request, self.template_name, {
            'user_form': user_form,
            'user_info_form': user_info_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        user_info_form = UserInfoForm(request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user_form.save()
            school = user_info_form.cleaned_data['school']
            school_obj, created = SchoolInfo.objects.get_or_create(school=school)
            user_info = request.user.userinfo
            user_info.school = school_obj
            user_info.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, self.template_name, {
                'user_form': user_form,
                'user_info_form': user_info_form
            })

def get_enrolled_list(request):
    user_id = request.user.id
    userinfo = UserInfo.objects.get(user_id=user_id)
    school = userinfo.school
    semester = userinfo.semester
    enrolled_list = student_enrolled.objects.filter(school=school, semester=semester)
    return userinfo,school, semester, enrolled_list


def student_enrolled_view(request):
    # user_id = request.user.id
    # userinfo = UserInfo.objects.get(user_id=user_id)
    # school = userinfo.school
    # semester = userinfo.semester
    # enrolled_list = student_enrolled.objects.filter(school=school, semester=semester)
    userinfo, school, semester, enrolled_list = get_enrolled_list(request)

    if request.method == 'POST':
        print("POST")
        form = student_enrolledForm(request.POST)
        if form.is_valid() and form.cleaned_data['not_enrolled']:
            print(form.cleaned_data['not_enrolled'])
            not_enrolled_lists = request.POST.get('not_enrolled').split(",")
            print(not_enrolled_lists)
            for not_enrolled in not_enrolled_lists:
                student_enroll_instance = student_enrolled()  # Instantiate a new model object
                student_enroll_instance.not_enrolled = not_enrolled
                student_enroll_instance.school = school
                student_enroll_instance.semester = semester
                student_enroll_instance.save()
        form = student_enrolledForm()

        context = {'form': form, 'enrolled_list': enrolled_list, "userinfo": userinfo}
        return render(request, 'base/student_enrolled.html', context)

    else:
        form = student_enrolledForm()

    context = {'form': form, 'enrolled_list': enrolled_list, "userinfo": userinfo}
    return render(request, 'base/student_enrolled.html', context)

def student_enrolled_list(request):
    print('list')
    user_id = request.user.id
    userinfo = UserInfo.objects.get(user_id=user_id)
    school = userinfo.school
    semester = userinfo.semester
    enrolled_list = student_enrolled.objects.filter(school=school, semester=semester)
    return render(request, 'base/student_enrolled_list.html', {'enrolled_list': enrolled_list})


def delete_enrolled(request, pk):
    student_enrolled.objects.filter(pk=pk).delete()
    return HttpResponse(f'<button class="badge badge-primary badge-pill" disabled>Deleted</button>')