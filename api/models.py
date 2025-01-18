from django.db import models
from django.contrib.auth.models import User


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
    student_year = models.IntegerField(blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True) 
    courses = models.ManyToManyField(Course, related_name='teachers', blank=True) 
    specialty = models.CharField(max_length=200, blank=True) 

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


 