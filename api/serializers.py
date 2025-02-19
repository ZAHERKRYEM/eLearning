from rest_framework import serializers
from .models import Course, Exam, Student, Subject,Teacher, Video,User
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
        fields = ['student_year', 'student_id']

  
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
        fields = ['student_year', 'student_id']


    
    def create(self, validated_data):

        teacher = Teacher.objects.create(**validated_data)

        return teacher

    def update(self, instance, validated_data):
        instance.student_year = validated_data.get('student_year', instance.student_year)
        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.save()
        return instance



class CourseSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id','subject','title','image','image_url','description','start_date','end_date','student_year','is_active']

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        return Subject.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


# class CourseSerializer(serializers.ModelSerializer):
#     subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

#     class Meta:
#         model = Course
#         fields = ['id', 'subject', 'title', 'description', 'start_date', 'end_date', 'is_active']

#     def create(self, validated_data):
#         return Course.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.subject = validated_data.get('subject', instance.subject)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.start_date = validated_data.get('start_date', instance.start_date)
#         instance.end_date = validated_data.get('end_date', instance.end_date)
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.save()
#         return instance


class ExamSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Exam
        fields = ['id', 'teacher', 'subject', 'title', 'date', 'duration', 'total_marks']

    def create(self, validated_data):
        return Exam.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.title = validated_data.get('title', instance.title)
        instance.date = validated_data.get('date', instance.date)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.total_marks = validated_data.get('total_marks', instance.total_marks)
        instance.save()
        return instance


class VideoSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = ['id', 'course', 'teacher', 'title', 'url', 'description', 'upload_date']

    def create(self, validated_data):
        return Video.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.course = validated_data.get('course', instance.course)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
