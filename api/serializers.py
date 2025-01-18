from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student,Teacher
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password',  'is_staff']

    def create(self, validated_data):
       
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_staff=validated_data['is_staff']
        )
        return user

    def update(self, instance, validated_data):
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'student_year', 'student_id']

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
   
        instance.student_year = validated_data.get('student_year', instance.student_year)
        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.save()
        return instance

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user', 'subjects', 'courses', 'specialty']

    def create(self, validated_data):
        return Teacher.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.specialty = validated_data.get('specialty', instance.specialty)
        instance.subjects.set(validated_data.get('subjects', instance.subjects.all()))
        instance.courses.set(validated_data.get('courses', instance.courses.all()))
        instance.save()
        return instance



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