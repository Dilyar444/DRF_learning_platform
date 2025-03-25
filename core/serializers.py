from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from .models import *

@extend_schema_serializer(component_name="User")
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_teacher', 'is_student']
        extra_kwargs = {
            'id': {'help_text': 'Уникальный идентификатор пользователя'},
            'username': {'help_text': 'Имя пользователя'},
            'is_teacher': {'help_text': 'Является ли пользователь преподавателем'},
            'is_student': {'help_text': 'Является ли пользователь студентом'},
        }

@extend_schema_serializer(component_name="Course")
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Уникальный идентификатор курса'},
            'title': {'help_text': 'Название курса'},
            'description': {'help_text': 'Описание курса'},
            'teacher': {'help_text': 'Идентификатор преподавателя'},
            'students': {'help_text': 'Список идентификаторов студентов, записанных на курс'},
            'created_at': {'help_text': 'Дата создания курса'},
        }

@extend_schema_serializer(component_name="Lesson")
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Уникальный идентификатор урока'},
            'course': {'help_text': 'Идентификатор курса, к которому относится урок'},
            'title': {'help_text': 'Название урока'},
            'content': {'help_text': 'Содержание урока'},
            'file': {'help_text': 'Файл с материалами урока (если есть)'},
        }

@extend_schema_serializer(component_name="Assignment")
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Уникальный идентификатор задания'},
            'lesson': {'help_text': 'Идентификатор урока, к которому относится задание'},
            'title': {'help_text': 'Название задания'},
            'description': {'help_text': 'Описание задания'},
            'deadline': {'help_text': 'Крайний срок сдачи задания'},
        }

@extend_schema_serializer(component_name="Submission")
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Уникальный идентификатор выполненного задания'},
            'assignment': {'help_text': 'Идентификатор задания'},
            'student': {'help_text': 'Идентификатор студента, который выполнил задание'},
            'file': {'help_text': 'Файл с выполненным заданием'},
            'submitted_at': {'help_text': 'Дата и время отправки задания'},
            'grade': {'help_text': 'Оценка за задание (если есть)'},
        }

@extend_schema_serializer(component_name="Review")
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Уникальный идентификатор отзыва'},
            'course': {'help_text': 'Идентификатор курса, на который оставлен отзыв'},
            'student': {'help_text': 'Идентификатор студента, оставившего отзыв'},
            'rating': {'help_text': 'Оценка курса (от 1 до 5)'},
            'comment': {'help_text': 'Комментарий к отзыву'},
        }