from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, UpdateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import pandas as pd
import numpy as np
from base.models import SchoolInfo, SemesterInfo, UserInfo, student_enrolled
from .models import ReferenceScore, ReferenceSubsubject, Reference_Grade_Subject
from .forms import UploadFileForm, ReferenceScoreForm, subject_subsubject_Form
from django.urls import reverse
# Create your views here.
#
def how_to(request):
    return render(request, 'score_check/how_to.html')
#
def score_check_select(request):
    user_id = request.user.id
    user_info =get_object_or_404(UserInfo, user_id=user_id)
    print(user_info.semester.id)
    grades = Reference_Grade_Subject.objects.filter(school=user_info.school.id, semester=user_info.semester.id).values('grade').distinct()
    enrollment_list = student_enrolled.objects.filter(school=user_info.school.id, semester=user_info.semester.id)
    enrollment_list = [enrollment.not_enrolled.split("-") for enrollment in enrollment_list]
    context={ 'grades': grades }
    if request.method == 'POST':
        학년 = request.POST.get('grade', None)
        과목 = request.POST.get('subject', None)
        영역 = request.POST.get('subsubject', None)
        if 과목 != None and 영역 != None:
            subsubject = ReferenceSubsubject.objects.get(id=영역)
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded = form.cleaned_data['file']
                reference_list = get_reference_list(subsubject)
                error_list = score_check_pandas(uploaded, reference_list, enrollment_list, grade=학년)
                reference_list = get_reference_list(subsubject)
                subsubjects = ReferenceSubsubject.objects.filter(subject_id=과목)  # Get subsubjects for selected subject
                subjects = Reference_Grade_Subject.objects.filter(grade=학년).values('subject').distinct()  # Get subjects for selected grade
                context = {
                    "grades": grades,
                    "subjects": subjects,
                    "subsubjects": subsubjects,  # Include subsubjects in context
                    "error_name": subsubject.subsubject + " " + " 오류목록",
                    "error_list": error_list,
                    "subsubject": subsubject,
                    "reference_list": reference_list
                }
                return render(request, 'score_check/score_check_select.html', context=context )
            else:
                context = {"grades": grades, "errors": "파일을 업로드해주세요."}
                return render(request, 'score_check/score_check_select.html', context=context)
        else:
            context = { "grades": grades, "errors":"과목과 영역을 선택해주세요." }
            return render(request, 'score_check/score_check_select.html', context=context)
    return render(request, 'score_check/score_check_select.html', context=context)
#
def score_check_pandas(uploaded, reference_list, enrollment_list,grade):
    uploaded_df = pd.read_excel(uploaded)
    class_list = list(uploaded_df.iloc[6, :][1:])
    class_index_dic = {i + 1: class_list[i] for i in range(len(class_list)) if type(class_list[i]) == int}
    class_index_dic[1] = 1

    error_list = []
    for index, row in uploaded_df.iterrows():
        index -= 6
        if type(row[1]) == int:
            score_lists = [row[i] for i in sorted(list(class_index_dic.keys()))]
            for i in range(1, len(score_lists)):
                score = score_lists[i]
                if np.isnan(score):
                    if [grade,str(i),str(index)] not in enrollment_list:
                        error_list.append(f"{i}반 {index}번 입력 없음")
                    else:
                        print("not enrolled")
                elif score not in reference_list:
                    error_list.append(f"{i}반 {index}번 점수 오류 ({score}점)")

    error_list = sorted(error_list, key=lambda x: (int(x.split()[0][:-1]), int(x.split()[1][:-1])))
    return error_list

def get_reference_list(subsubject):
    reference_list = ReferenceScore.objects.filter(subsubject_id=subsubject)
    print(reference_list)
    scores = [list(map(int,reference.score_list.split())) for reference in reference_list]

    print("scores" ,scores)
    result = summation(scores)
    print("result", result)
    return result

def summation(add_list) :
    sum_list=[]
    while add_list:
        if sum_list: add1 = [a for a in sum_list]
        else: add1 = add_list.pop(0)
        try: add2 = add_list.pop(0)
        except:
            sum_list = add1
            break
        sum_list.clear()
        for a in add1:
            for b in add2:
                if a + b not in sum_list: sum_list.append(a + b)
    return sum_list
#
def get_subsubjects(request):
    subject = request.GET.get('subject', None)
    if subject:
        subsubjects = ReferenceSubsubject.objects.filter(subject_id=subject)
    else:
        subsubjects = []

    url = reverse('score_check:subsubject_id')
    html = "<label>&nbsp;&nbsp;영역&nbsp;</label>"
    html += f'<select name="subsubject" id="subsubject" hx-get="{url}" hx-target="#subsubject_idcheck">'
    html += "<option value='' selected>영역을 선택해주세요</option>"

    for subsubject in subsubjects:
        html += f"<option value='{subsubject.id}'>{subsubject.subsubject}</option>"

    html += "</select>"

    return HttpResponse(html)


#
def get_subjects(request):
    grade = request.GET.get('grade', None)
    user_info = get_object_or_404(UserInfo, user_id=request.user.id)
    if grade:
        subjects = Reference_Grade_Subject.objects.filter(grade=grade, school=user_info.school.id, semester=user_info.semester.id)
    else:
        subjects = []

    url = reverse('score_check:get_subsubjects')
    html = "<label>&nbsp;&nbsp;&nbsp;&nbsp;과목&nbsp;</label>"
    html += f'<select name="subject" id="subject" hx-get="{url}" hx-target="#subsubject">'
    html += "<option value='' selected>과목을 선택해주세요</option>"
    for subject in subjects:
        html += f"<option value='{subject.id}'>{subject.subject}</option>"
    html += "</select>"

    return HttpResponse(html)



def add_reference(request):
    user_id = request.user.id
    user_info = get_object_or_404(UserInfo, user_id=user_id)
    grades = Reference_Grade_Subject.objects.filter(school=user_info.school.id, semester=user_info.semester.id).values(
        'grade').distinct()
    context = {"form": ReferenceScoreForm(),
               "grades": grades,
               "score_Form": ReferenceScoreForm()}
    return render(request, 'score_check/add_reference.html',context=context)

def add_reference_score(request):
    subsubject_id = request.GET.get('subsubject_id', None)
    if request.method == 'POST':
        form = ReferenceScoreForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('score_check:add_reference')
        else:
            print(form.errors)
            return render(request, 'score_check/add_reference.html', context={"score_Form": form})
    context = {"score_Form": ReferenceScoreForm(), "subsubject_id":subsubject_id}
    return render(request, 'score_check/add_reference_score.html',context=context)

def subsubject_id(request):
    subsubject_id = request.GET.get('subsubject', None)
    html = f"<input type ='hidden' name='subsubject_idchecktt' value='{subsubject_id}' id='subsubject_idchecktt'>"
    return HttpResponse(html)


def create_reference_subject(request):
    form = subject_subsubject_Form()
    return render(request, 'score_check/create_reference_subject.html', {'form': form})


def reference_list(request):
    user_id = request.user.id
    user_info = get_object_or_404(UserInfo, user_id=user_id)
    subjects = Reference_Grade_Subject.objects.filter(school=user_info.school.id, semester=user_info.semester.id).order_by('grade','subject')
    subject_id = request.GET.get('subject_id')
    if subject_id:
        selected_subject = Reference_Grade_Subject.objects.get(id=subject_id)
        subsubjects = ReferenceSubsubject.objects.filter(subject_id=subject_id)

        # Make sure that each QuerySet is evaluated to a list
        scores = [list(ReferenceScore.objects.filter(subsubject=subsubject).order_by('score_name')) for subsubject in subsubjects]

        # Zip subsubjects and scores together
        subsubjects_scores = zip(subsubjects, scores)
    else:
        selected_subject = None
        subsubjects_scores = None

    return render(request, 'score_check/reference_list.html', {
        'subjects': subjects,
        'selected_subject': selected_subject,
        'subsubjects_scores': subsubjects_scores,
    })

def create_reference_subsubject(request):
    grade = request.GET.get('grade', None)
    subject = request.GET.get('subject', None)
    if request.method == 'POST':

        form = subject_subsubject_Form(request.POST or None, request=request)
        if form.is_valid():
            form.save()
            return redirect('score_check:create_reference_subject')
        else:
            print(form.errors)
            return render(request, 'score_check/create_reference_subject.html', context={"form": form})
    form = subject_subsubject_Form(request=request)
    context = {"form": form, "grade":grade, "subject":subject}
    return render(request, 'score_check/create_reference_subsubject.html', context=context)



def Reference_list_delete(request, pk):
    ReferenceSubsubject.objects.filter(pk=pk).delete()
    # something about warning

    return HttpResponse(f'<button disabled>삭제됨</button>')

def Reference_list_update(request, pk):
    subsubject = ReferenceSubsubject.objects.get(pk=pk)
    scores = ReferenceScore.objects.filter(subsubject=subsubject).order_by('score_name')
    return render(request, 'score_check/reference_list_update.html', {'scores': scores, 'pk': pk})


def Reference_list_update_instance(request, pk):
    score_name = request.POST.get('score_name', None)
    score_list = request.POST.get('score_list', None)
    subsubject_pk = request.POST.get('subsubject', None)
    score_id = request.POST.get('score_id', None)
    print(score_name, score_list, subsubject_pk)
    # Get the ReferenceSubsubject instance
    subsubject = ReferenceSubsubject.objects.get(pk=subsubject_pk)

    score = ReferenceScore.objects.get(pk = score_id)
    score.score_name = score_name
    score.score_list = score_list
    score.subsubject = subsubject  # assign the ReferenceSubsubject instance
    score.save()
    # return HttpResponse(f'<button disabled>수정됨</button>')

    return render(request, 'score_check/reference_list_update.html', {'scores': [score], 'pk': pk})
