from django.urls import path
from . import views



app_name = 'score_check'



urlpatterns=[
    path('how_to/', views.how_to, name='how_to'),
    path('score_check/', views.score_check_select, name='score_check'),
    path('add_reference/', views.add_reference, name='add_reference'),
    path('reference_list/', views.reference_list, name='reference_list'),
    path('create_reference_subject/', views.create_reference_subject, name='create_reference_subject'),
    # path('Reference_list_update/', views.Reference_list_update, name='Reference_list_update'),

    ]


htmx_urlpatterns = [
    path('get_subsubjects/', views.get_subsubjects, name='get_subsubjects'),
    path('get_subjects/', views.get_subjects, name='get_subjects'),
    path('add_reference_score/', views.add_reference_score, name='add_reference_score'),
    path('subsubject_id/', views.subsubject_id, name='subsubject_id'),
    path('create_reference_subsubject/', views.create_reference_subsubject, name='create_reference_subsubject'),
    path('Reference_list_delete/<int:pk>/', views.Reference_list_delete, name='Reference_list_delete'),
    path('Reference_list_update/<int:pk>/', views.Reference_list_update, name='Reference_list_update'),
    path('Reference_list_update_instance/<int:pk>/', views.Reference_list_update_instance, name='Reference_list_update_instance'),
    # path('create_subsubject/', views.create_subsubject, name='create_subsubject'),
]

urlpatterns = urlpatterns + htmx_urlpatterns
