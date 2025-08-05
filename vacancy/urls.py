from django.urls import path
from vacancy.views import *


urlpatterns = [
    path('',vacancy_list,name='vacancy'),
    path('create/',create_vacancy,name='create_vacancy'),
    path('update/<int:id>/',update_vacancy,name='update_vacancy'),
    path('delete/<int:id>/',delete_vacancy,name='delete_vacancy'),
    path('vacancylist/',vacancy_applicants_list, name='vacancy_applicants_list'),
    path('apply/<int:vacancy_id>/',apply_for_vacancy,name='apply_vacancy'),
    path('applicant-details/<int:id>/',applicant_details,name='applicant_details'),
    path('applicant/schedule/<int:id>/',schedule_interview,name='schedule'),
    path('reject/<int:id>/',reject_applicant,name='reject'),
    path('filter/<int:id>/',filter_applicants,name='filter'),
    path('filter/list/',filter_list,name='filter_list'),
    path('filter/details/<int:interview_id>/applicant/<int:applicant_id>/',filter_appplicant_details,name='filter-details'),
    path('hire/<int:interview_id>/applicant/<int:applicant_id>/',hire_applicant,name='hire'),
    path('filter/reject/<int:applicant_id>/',delete_applicant_completely,name='delete_filter')
]