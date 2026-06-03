from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Course and lesson URLs
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    
    # Exam URLs
    path('exam/', views.exam_view, name='exam'),
    path('submit/<int:question_id>/', views.submit, name='submit'),
    path('exam/result/', views.show_exam_result, name='show_exam_result'),
]