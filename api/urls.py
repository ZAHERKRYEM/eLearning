from django.urls import path  
from .views import StudentCreateView ,LoginView ,LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [  
    path('register/', StudentCreateView.as_view(), name='register_user'),  
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

]