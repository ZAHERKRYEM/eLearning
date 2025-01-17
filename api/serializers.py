from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password', 'email','is_staff']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'student_year', 'student_id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student, created = Student.objects.get_or_create(user=user, **validated_data)

       
        refresh = RefreshToken.for_user(user)
        
        return {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_staff':user.is_staff
        }


# class SubjectSerializer(serializers.ModelSerializer):  
#     class Meta:  
#         model = Subject  
#         fields = ['id', 'name', 'description']  


# class CourseSerializer(serializers.ModelSerializer):  
#     subject = SubjectSerializer()   

#     class Meta:  
#         model = Course  
#         fields = ['id', 'subject', 'title', 'description', 'start_date', 'end_date']  


# class StudentSerializer(serializers.ModelSerializer):  
#     courses = CourseSerializer(many=True)  
#     subject = SubjectSerializer()  

#     class Meta:  
#         model = Student  
#         fields = ['id', 'user', 'courses', 'subject']  


# class TeacherSerializer(serializers.ModelSerializer):  
#     subject = SubjectSerializer()  

#     class Meta:  
#         model = Teacher  
#         fields = ['id', 'user', 'subject']  


# class ExamSerializer(serializers.ModelSerializer):  
#     class Meta:  
#         model = Exam  
#         fields = ['id', 'title', 'date', 'duration', 'total_marks']  


# class VideoSerializer(serializers.ModelSerializer):  
#     course = CourseSerializer()  
#     teacher = TeacherSerializer()  

#     class Meta:  
#         model = Video  
#         fields = ['id', 'course', 'teacher', 'title', 'url', 'description']