from django.urls import path
from . import views

app_name = 'base'

urlpatterns=[
    path('',views.main_view, name='main'),
    path('my_page/',views.my_page_view.as_view(), name='my_page'),
    path('student_enrolled/',views.student_enrolled_view, name='student_enrolled'),
    path('dev_info/',views.dev_info_view, name='dev_info'),
    ]

htmx_urlpatterns = [
    path('studnet_enrolled_list/', views.student_enrolled_list, name='student_enrolled_list'),
    path('delete_enrolled/<int:pk>/', views.delete_enrolled, name='delete_enrolled'),
    ]

urlpatterns = urlpatterns + htmx_urlpatterns