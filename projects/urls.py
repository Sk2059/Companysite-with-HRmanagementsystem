from django.urls import path
from . import views

urlpatterns = [
    path('service-list/', views.Servicelist_list, name='service-list'),
    path('create-service/', views.create_service, name='create-service'),
    path('update-service/<int:id>/', views.update_service, name='update-service'),
    path('delete-service/<int:id>/', views.delete_service, name='delete-service'),
    path('delete-project/<int:id>/', views.delete_project, name='delete-project'),
    path('create-project/<int:id>/', views.create_project, name='create-project'),
    path('project-list/', views.project_list, name='project-list'),
    path('create-startproject/<int:id>/', views.create_startproject, name='create-startproject'),
    path('update-startproject/<int:id>/', views.update_startproject, name='update-startproject'),
    path('startproject-list/', views.startproject_list, name='startproject-list'),
    path('deploy-project/<int:id>/', views.deploy_project, name='deploy-project'),
    path('deploy-list/', views.deploy_list, name='deploy-list'),
    path('delete-deployed-project/<int:id>/', views.delete_deployed_project, name='delete-deployed-project'),
    path('deleted-startprojejct/<int:id>/',views.delete_startproject,name='delete-startproject')
]
