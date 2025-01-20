from rest_framework import status
from rest_framework.response import Response
from .models import Student, Teacher
from .serializers import TeacherSerializer, UserSerializer,StudentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView



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
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subject, Course, Exam, Video
from .serializers import SubjectSerializer, CourseSerializer, ExamSerializer, VideoSerializer

class SubjectAPIView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response({
            "status": True,
            "data": serializer.data,
            "message": "Subjects retrieved successfully",
            "status_code": 200
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            return Response({
                "status": True,
                "data": SubjectSerializer(subject).data,
                "message": "Subject created successfully",
                "status_code": 201
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Subject creation failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({
                "status": False,
                "message": "Subject not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            return Response({
                "status": True,
                "data": SubjectSerializer(subject).data,
                "message": "Subject updated successfully",
                "status_code": 200
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Subject update failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
            subject.delete()
            return Response({
                "status": True,
                "message": "Subject deleted successfully",
                "status_code": 204
            }, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist:
            return Response({
                "status": False,
                "message": "Subject not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)

# Similar views for Course, Exam, Video with the same structure

class CourseAPIView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response({
            "status": True,
            "data": serializer.data,
            "message": "Courses retrieved successfully",
            "status_code": 200
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response({
                "status": True,
                "data": CourseSerializer(course).data,
                "message": "Course created successfully",
                "status_code": 201
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Course creation failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({
                "status": False,
                "message": "Course not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response({
                "status": True,
                "data": CourseSerializer(course).data,
                "message": "Course updated successfully",
                "status_code": 200
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Course update failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({
                "status": True,
                "message": "Course deleted successfully",
                "status_code": 204
            }, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({
                "status": False,
                "message": "Course not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)

# Repeat similar structure for ExamAPIView and VideoAPIView.
class ExamAPIView(APIView):
    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response({
            "status": True,
            "data": serializer.data,
            "message": "Exams retrieved successfully",
            "status_code": 200
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            exam = serializer.save()
            return Response({
                "status": True,
                "data": ExamSerializer(exam).data,
                "message": "Exam created successfully",
                "status_code": 201
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Exam creation failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response({
                "status": False,
                "message": "Exam not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ExamSerializer(exam, data=request.data)
        if serializer.is_valid():
            exam = serializer.save()
            return Response({
                "status": True,
                "data": ExamSerializer(exam).data,
                "message": "Exam updated successfully",
                "status_code": 200
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Exam update failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
            exam.delete()
            return Response({
                "status": True,
                "message": "Exam deleted successfully",
                "status_code": 204
            }, status=status.HTTP_204_NO_CONTENT)
        except Exam.DoesNotExist:
            return Response({
                "status": False,
                "message": "Exam not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)
class VideoAPIView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response({
            "status": True,
            "data": serializer.data,
            "message": "Videos retrieved successfully",
            "status_code": 200
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            return Response({
                "status": True,
                "data": VideoSerializer(video).data,
                "message": "Video created successfully",
                "status_code": 201
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Video creation failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({
                "status": False,
                "message": "Video not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            return Response({
                "status": True,
                "data": VideoSerializer(video).data,
                "message": "Video updated successfully",
                "status_code": 200
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "data": serializer.errors,
            "message": "Video update failed",
            "status_code": 400
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
            video.delete()
            return Response({
                "status": True,
                "message": "Video deleted successfully",
                "status_code": 204
            }, status=status.HTTP_204_NO_CONTENT)
        except Video.DoesNotExist:
            return Response({
                "status": False,
                "message": "Video not found",
                "status_code": 404
            }, status=status.HTTP_404_NOT_FOUND)
