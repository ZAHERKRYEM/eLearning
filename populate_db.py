import os  
import django  
from faker import Faker  

# إعداد Django  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  
django.setup()  

from api.models import Subject, Course, Student, Teacher, Exam, Video  
from django.contrib.auth.models import User  

fake = Faker()  

def populate(n=10):  
    for _ in range(n):  
        # إنشاء موضوع  
        subject = Subject.objects.create(  
            name=fake.word().capitalize(),  
            description=fake.text())  
        
        # إنشاء مستخدم للطالب  
        user_student = User.objects.create_user(  
            username=fake.user_name(),  
            password='password123'  
        )  
        student = Student.objects.create(  
            user=user_student,  
            subject=subject  
        )  
        
        # إنشاء مستخدم للمعلم  
        user_teacher = User.objects.create_user(  
            username=fake.user_name(),  
            password='password123'  
        )  
        teacher = Teacher.objects.create(  
            user=user_teacher,  
            subject=subject  
        )  
        
        # إنشاء دورات  
        course = Course.objects.create(  
            subject=subject,  
            title=fake.catch_phrase(),  
            description=fake.text(),  
            start_date=fake.date_this_year(),  
            end_date=fake.date_this_year()  
        )  
        
        # إنشاء امتحانات  
        exam = Exam.objects.create(  
            title=fake.sentence(),  
            date=fake.date_time_this_year(),  
            duration=fake.random_int(min=30, max=180),  
            total_marks=fake.random_int(min=50, max=100)  
        )  

        # ربط الطالب بالدورة والامتحان  
        student.courses.add(course)  
        student.exams_taken.add(exam)  
        
        # إنشاء فيديو  
        Video.objects.create(  
            course=course,  
            teacher=teacher,  
            title=fake.sentence(),  
            url=fake.url(),  
            description=fake.text()  
        )  

    print(f'{n} records have been added to the database.')  

if __name__ == '__main__':  
    populate(10)  # يمكنك تغيير العدد إلى أي رقم تريده