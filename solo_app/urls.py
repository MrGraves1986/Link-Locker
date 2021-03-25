from django.urls import path
from . import views
# from .views import contact_form, submit_message

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('link_page', views.link_page),
    path('logout', views.logout),
    path('create_link', views.create_link),
    path('success_page', views.success_page),
    path('delete_link/<int:link_id>', views.delete_link),
    path('contact/', views.contact),
    path('back', views.back),
    path('contact_form', views.contact_form),
    path('submit_message', views.submit_message),
    # path('link.content', views.new_page),
]





