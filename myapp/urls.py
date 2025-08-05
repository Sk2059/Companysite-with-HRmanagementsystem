from django.urls import path
from myapp.views import *
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/',login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('',employee_list,name='employee-list'),
    path('create/',create_employee,name='create'),
    path('details/<id>/',employee_details,name='details'),
    path('update/<id>/',update_employee,name='update'),
    path('delete/<id>/',delete_employee,name='delete')
]