from django.urls import path  
from .views import AllCoursesView, CourseByYearView, CourseSearchView, OneCoursePerYearView, TeacherAPIView,Refreshtoken, UserCreateAPIView,UserDetailAPIView ,LoginView ,LogoutView,StudentAPIView,SubjectAPIView, CourseAPIView, ExamAPIView, VideoAPIView


urlpatterns = [  
    path('register/', UserCreateAPIView.as_view(), name='user-create'),
    path('students/', StudentAPIView.as_view(), name='student-create'),
    path('users/', UserDetailAPIView.as_view(), name='user-detail'), 
    path('teacher/', TeacherAPIView.as_view(), name='teacher'),

    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', Refreshtoken.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('courses/search/', CourseSearchView.as_view(), name='course_search'),
    path('courses/by-year/', CourseByYearView.as_view(), name='course_by_year'),
    path('courses/one-per-year/', OneCoursePerYearView.as_view(), name='one_course_per_year'),
    path('courses/all/', AllCoursesView.as_view(), name='all_courses'),




     path('subjects/', SubjectAPIView.as_view(), name='subjects'),
    path('courses/', CourseAPIView.as_view(), name='courses'),
    path('exams/', ExamAPIView.as_view(), name='exams'),
    path('videos/', VideoAPIView.as_view(), name='videos'),

]