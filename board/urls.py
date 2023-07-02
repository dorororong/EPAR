from django.urls import path
from . import views

app_name='board'

urlpatterns = [
    path('<int:pk>/', views.posting_view, name='posting'),
    path('new_post/', views.new_post_view, name='new_post'),
    path('', views.board_main_view, name='board'),
    path('post/<int:pk>/update/', views.update_post_view, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post_view, name='delete_post'),
]