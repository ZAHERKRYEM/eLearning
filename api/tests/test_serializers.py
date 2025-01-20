from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Teacher, Video
from api.serializers import UserSerializer, VideoSerializer

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")

    def test_update_user(self):
        data = {"username": "updateduser", "email": "updateduser@example.com"}
        serializer = UserSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), msg=f"Serializer errors: {serializer.errors}")
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updateduser@example.com")


class VideoSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teacheruser", email="teacher@example.com", password="password123")
        self.teacher = Teacher.objects.create(user=self.user, student_year="Year 1", student_id=2001)
        self.video_data = {
            "title": "Test Video",
            "description": "A sample video description",
            "teacher": self.teacher.id,  # Use the teacher's ID for relation
            "url": "http://example.com/video.mp4",
        }

    def test_create_video(self):
        serializer = VideoSerializer(data=self.video_data)
        self.assertTrue(serializer.is_valid(), msg=f"Serializer errors: {serializer.errors}")
        video = serializer.save()
        self.assertEqual(video.title, "Test Video")
        self.assertEqual(video.description, "A sample video description")
        self.assertEqual(video.teacher, self.teacher)
        self.assertEqual(video.url, "http://example.com/video.mp4")

    def test_update_video(self):
        video = Video.objects.create(
            title="Old Video",
            description="Old description",
            teacher=self.teacher,
            url="http://example.com/old_video.mp4",
        )
        update_data = {"title": "Updated Video", "description": "Updated description"}
        serializer = VideoSerializer(instance=video, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), msg=f"Serializer errors: {serializer.errors}")
        updated_video = serializer.save()
        self.assertEqual(updated_video.title, "Updated Video")
        self.assertEqual(updated_video.description, "Updated description")


class TeacherModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teacheruser", email="teacher@example.com", password="password123")

    def test_create_teacher(self):
        teacher = Teacher.objects.create(user=self.user, student_year="Year 1", student_id=2001)
        self.assertEqual(teacher.user, self.user)
        self.assertEqual(teacher.student_year, "Year 1")
        self.assertEqual(teacher.student_id, 2001)
