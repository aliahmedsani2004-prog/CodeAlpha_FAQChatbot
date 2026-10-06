from django.contrib import admin
from django.urls import path
from faq_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.chat_page, name='chat'),
    path('ask/', views.ask, name='ask'),
]