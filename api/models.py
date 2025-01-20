from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('username', None)  # Ensure username can be None
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)  # Optional username

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Primary identifier
    REQUIRED_FIELDS = []  # No additional fields required for superuser creation

    def __str__(self):
        return self.email


class Subject(models.Model):  
    name = models.CharField(max_length=200)  
    description = models.TextField(blank=True)  

    def __str__(self):
        return self.name
    
class Course(models.Model):   
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)   
    title = models.CharField(max_length=200)    
    description = models.TextField(blank=True)  
    start_date = models.DateField()              
    end_date = models.DateField()              
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.title



class Exam(models.Model):
    teacher = models.ForeignKey('Teacher', related_name='exams', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='Subject', on_delete=models.CASCADE)      
    title = models.CharField(max_length=200)   
    date = models.DateTimeField()              
    duration = models.PositiveIntegerField()    
    total_marks = models.PositiveIntegerField() 
  

    def __str__(self):
        return self.title





class Student(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    courses = models.ManyToManyField(Course, related_name='students', blank=True)   
    exams_taken = models.ManyToManyField(Exam, related_name='students', blank=True) 
    student_year = models.CharField(max_length=20,blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True) 
    courses = models.ManyToManyField(Course, related_name='teachers', blank=True) 
    specialty = models.CharField(max_length=200, blank=True, null=True) 
    student_year = models.CharField(max_length=20,blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Video(models.Model):  
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)   
    teacher = models.ForeignKey(Teacher, related_name='videos', on_delete=models.CASCADE)   
    title = models.CharField(max_length=200)    
    url = models.URLField()                    
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title


 