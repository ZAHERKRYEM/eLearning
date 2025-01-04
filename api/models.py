from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):  
    name = models.CharField(max_length=200)  
    description = models.TextField(blank=True)  

class Exam(models.Model):  
    title = models.CharField(max_length=200)   
    date = models.DateTimeField()              
    duration = models.PositiveIntegerField()    
    total_marks = models.PositiveIntegerField() 




class Course(models.Model):  
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)   
    title = models.CharField(max_length=200)    
    description = models.TextField(blank=True)  
    start_date = models.DateField()              
    end_date = models.DateField()              


class Student(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    courses = models.ManyToManyField(Course, related_name='rolls_in')   
    exams_taken = models.ManyToManyField(Exam, related_name='takes') 
    subject = models.ForeignKey(Subject, related_name='have', on_delete=models.CASCADE) 
    
class Teacher(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    subject = models.ForeignKey(Subject, related_name='teachers', on_delete=models.CASCADE)  


class Video(models.Model):  
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)   
    teacher = models.ForeignKey(Teacher, related_name='uploads', on_delete=models.CASCADE)   
    title = models.CharField(max_length=200)    
    url = models.URLField()                    
    description = models.TextField(blank=True) 



 