from django.urls import path
from collab.views import *

urlpatterns = [
    path('collab/',create_collab,name='create_collab'),
    path('collab/list',collab_list,name='collab_list'),
    path('collab/delete/<int:id>',delete_collab,name='delete_collab'),
    path('partner/create/<int:id>/',create_partner,name='create_partner'),
    path('partner/',partners_list,name='partner_list'),
    path('partner/delete/<int:id>/',delete_partner,name='delete_partner'),
    # path('contact/',create_contact,name='create_contact'),
    path('contact/list',contact_list,name='contact_list'),
    path('contact/delete/<int:id>',delete_contact,name='delete_contact'),
    
]
