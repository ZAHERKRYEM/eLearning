from rest_framework import generics,status
from rest_framework.response import Response
from .models import Student, Teacher
from .serializers import TeacherSerializer, UserSerializer,StudentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User


class UserCreateAPIView(APIView):
    def post(self, request):
        user_data = request.data.get('user')  
        profile_data = request.data.get('profile') 
        is_staff = user_data.get('is_staff', False)  


        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()

  
            if is_staff:
                serializer = TeacherSerializer(data=profile_data)
            else:
                serializer = StudentSerializer(data=profile_data)

            if serializer.is_valid():

                profile = serializer.save(user=user)

             
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response({
                    "status": True,
                    "data": {
                        "user": user_serializer.data,
                        "profile": serializer.data,
                        "tokens": tokens
                    },
                    "message": "User and profile created successfully",
                    "status_code": 201
                }, status=status.HTTP_201_CREATED)

            return Response({
                "status": False,
                "data": serializer.errors,
                "message": "Profile creation failed",
                "status_code": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": False,
            "data": user_serializer.errors,
            "message": "User creation failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
  
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user  
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user  
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class StudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
     
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
          
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeacherAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Access denied. Only staff members can access this.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Access denied. Only staff members can create teachers.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
 
        if not request.user.is_staff:
            return Response({'error': 'Access denied. Only staff members can update teachers.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class LoginView(TokenObtainPairView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": True,
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                "message": "Login successful",
                "status_code": 200
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "data": {},
                "message": "Invalid credentials",
                "status_code": 401
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "status": True,
                "data": {},
                "message": "Successfully logged out",
                "status_code": 205
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                "status": False,
                "data": {},
                "message": str(e),
                "status_code": 400
            }, status=status.HTTP_400_BAD_REQUEST)
