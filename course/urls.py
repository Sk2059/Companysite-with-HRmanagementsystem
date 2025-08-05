from django.urls import path
from . import views

urlpatterns = [
    # path('', views.course_list, name='course_list'),
    # path('<int:id>/', views.course_detail, name='course_detail'),
    path('add/', views.add_course, name='add_course'),
    path('register/', views.register_course, name='course_register'),
    path('register/<int:id>/', views.register_course, name='course_register'),
    path('submissions/', views.course_submissions, name='course_submissions'),
    path('submissions/delete/<int:pk>/', views.delete_registration, name='delete_registration'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
]
