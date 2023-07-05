from django.urls import path
from . import views



app_name = 'score_check'



urlpatterns=[
    path('how_to/', views.how_to, name='how_to'),

    ]


htmx_urlpatterns = [
]

urlpatterns = urlpatterns + htmx_urlpatterns