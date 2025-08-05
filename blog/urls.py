from django.urls import path
from blog.views import *
urlpatterns = [
    path('create/',create_blog,name='create_blog'),
    path('update/<int:id>/',update_blog,name='update_blog'),
    path('',blog_lists,name='blog_lists'),
    path('delete/<int:id>/',delete_blog,name='delete_blog')
]