from django.urls import path
from .views import *
from vacancy.views import *
from projects.views import *
from collab.views import *
from blog.views import *


urlpatterns = [
    path('',home,name='home'),
    path('blogs/', blogs, name='blogs'),
    path('blogs/<int:id>/',read_blog, name='read_blog'),
    path('careers/', careers, name='careers'),
    path('contact/',create_contact,name='contact'),
    path('services/',service_list_frontt,name='service_list'),
    path('applicant/<int:id>/',application_form, name='applicant'),
    path('about/',about,name='about'),
    path('collab/',create_collab,name='collab'),
    path('development/',development_services,name='development'),
    path('developent/<int:id>/',service_form,name='service_form'),
    path('Digitalmarketing_form/',marketing_services,name='Digitalmarketing_form'),
    path('digital-marketing/combo/',combo_packages, name='combo_packages'),
    path('courses/',courses,name='courses'),
    path('course_registration/',course_registration,name='course_registration'),
    path('testimonial/',submit_testimonial,name='testimonial-form'),
    path('testimonial/form/', submit_testimonial, name='testimonial'),
    path('testimonials/', testimonial_list, name='testimonial-list'),
    path('testimonials/<int:testimonial_id>/delete/', delete_testimonial, name='delete_testimonial'),
    path('course/<int:course_id>/',course_detail, name='course_detail'),
]
