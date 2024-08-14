from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('courses/', views.get_courses),
    path('courses/<str:id>', views.get_course)
]