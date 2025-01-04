from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import (  
    SubjectViewSet,  
    CourseViewSet,  
    StudentViewSet,  
    TeacherViewSet,  
    ExamViewSet,  
    VideoViewSet  
)  

router = DefaultRouter()  
router.register(r'subjects', SubjectViewSet)  
router.register(r'courses', CourseViewSet)  
router.register(r'students', StudentViewSet)  
router.register(r'teachers', TeacherViewSet)  
router.register(r'exams', ExamViewSet)  
router.register(r'videos', VideoViewSet)  

urlpatterns = [  
    path('', include(router.urls)),  
]