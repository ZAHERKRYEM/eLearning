from django.urls import path  
from .views import TeacherAPIView, UserCreateAPIView,UserDetailAPIView ,LoginView ,LogoutView,StudentAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [  
    path('register/', UserCreateAPIView.as_view(), name='user-create'),
    path('students/', StudentAPIView.as_view(), name='student-create'),
    path('users/', UserDetailAPIView.as_view(), name='user-detail'), 
    path('teacher/', TeacherAPIView.as_view(), name='teacher'),

    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

]