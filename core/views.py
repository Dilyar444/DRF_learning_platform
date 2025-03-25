from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import *
from .serializers import *
from .permissions import IsTeacherOrReadOnly

@extend_schema_view(
    list=extend_schema(summary="Получить список курсов", description="Возвращает список всех доступных курсов.", tags=["Курсы"]),
    create=extend_schema(summary="Создать новый курс", description="Создает новый курс. Доступно только преподавателям.", tags=["Курсы"]),
    retrieve=extend_schema(summary="Получить информацию о курсе", description="Возвращает информацию о курсе по его ID.", tags=["Курсы"]),
    update=extend_schema(summary="Обновить курс", description="Обновляет данные курса по его ID. Доступно только преподавателям.", tags=["Курсы"]),
    partial_update=extend_schema(summary="Частично обновить курс", description="Частично обновляет данные курса по его ID. Доступно только преподавателям.", tags=["Курсы"]),
    destroy=extend_schema(summary="Удалить курс", description="Удаляет курс по его ID. Доступно только преподавателям.", tags=["Курсы"]),
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]

    @extend_schema(summary="Записаться на курс", description="Позволяет студенту записаться на курс по его ID.", tags=["Курсы"])
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'status': 'enrolled'})

@extend_schema_view(
    list=extend_schema(summary="Получить список уроков", description="Возвращает список всех уроков.", tags=["Уроки"]),
    create=extend_schema(summary="Создать новый урок", description="Создает новый урок для курса. Доступно только преподавателям.", tags=["Уроки"]),
    retrieve=extend_schema(summary="Получить информацию об уроке", description="Возвращает информацию об уроке по его ID.", tags=["Уроки"]),
    update=extend_schema(summary="Обновить урок", description="Обновляет данные урока по его ID. Доступно только преподавателям.", tags=["Уроки"]),
    partial_update=extend_schema(summary="Частично обновить урок", description="Частично обновляет данные урока по его ID. Доступно только преподавателям.", tags=["Уроки"]),
    destroy=extend_schema(summary="Удалить урок", description="Удаляет урок по его ID. Доступно только преподавателям.", tags=["Уроки"]),
)
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrReadOnly]

@extend_schema_view(
    list=extend_schema(summary="Получить список заданий", description="Возвращает список всех заданий.", tags=["Задания"]),
    create=extend_schema(summary="Создать новое задание", description="Создает новое задание для урока. Доступно только преподавателям.", tags=["Задания"]),
    retrieve=extend_schema(summary="Получить информацию о задании", description="Возвращает информацию о задании по его ID.", tags=["Задания"]),
    update=extend_schema(summary="Обновить задание", description="Обновляет данные задания по его ID. Доступно только преподавателям.", tags=["Задания"]),
    partial_update=extend_schema(summary="Частично обновить задание", description="Частично обновляет данные задания по его ID. Доступно только преподавателям.", tags=["Задания"]),
    destroy=extend_schema(summary="Удалить задание", description="Удаляет задание по его ID. Доступно только преподавателям.", tags=["Задания"]),
)
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherOrReadOnly]

@extend_schema_view(
    list=extend_schema(summary="Получить список выполненных заданий", description="Возвращает список всех выполненных заданий.", tags=["Выполненные задания"]),
    create=extend_schema(summary="Отправить выполненное задание", description="Позволяет студенту отправить выполненное задание.", tags=["Выполненные задания"]),
    retrieve=extend_schema(summary="Получить информацию о выполненном задании", description="Возвращает информацию о выполненном задании по его ID.", tags=["Выполненные задания"]),
    update=extend_schema(summary="Обновить выполненное задание", description="Обновляет данные выполненного задания по его ID.", tags=["Выполненные задания"]),
    partial_update=extend_schema(summary="Частично обновить выполненное задание", description="Частично обновляет данные выполненного задания по его ID.", tags=["Выполненные задания"]),
    destroy=extend_schema(summary="Удалить выполненное задание", description="Удаляет выполненное задание по его ID.", tags=["Выполненные задания"]),
)
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

@extend_schema_view(
    list=extend_schema(summary="Получить список отзывов", description="Возвращает список всех отзывов на курсы.", tags=["Отзывы"]),
    create=extend_schema(summary="Оставить отзыв на курс", description="Позволяет студенту оставить отзыв на курс.", tags=["Отзывы"]),
    retrieve=extend_schema(summary="Получить информацию об отзыве", description="Возвращает информацию об отзыве по его ID.", tags=["Отзывы"]),
    update=extend_schema(summary="Обновить отзыв", description="Обновляет данные отзыва по его ID.", tags=["Отзывы"]),
    partial_update=extend_schema(summary="Частично обновить отзыв", description="Частично обновляет данные отзыва по его ID.", tags=["Отзывы"]),
    destroy=extend_schema(summary="Удалить отзыв", description="Удаляет отзыв по его ID.", tags=["Отзывы"]),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer