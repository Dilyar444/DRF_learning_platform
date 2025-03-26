from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import *
from .serializers import *
from .permissions import IsTeacherOrReadOnly, IsOwnerOrTeacher, IsEnrolledOrTeacher, CanReviewCourse

@extend_schema_view(
    list=extend_schema(summary="Получить список курсов", description="Возвращает список всех доступных курсов.", tags=["Курсы"]),
    create=extend_schema(summary="Создать новый курс", description="Создает новый курс. Доступно только преподавателям.", tags=["Курсы"]),
    retrieve=extend_schema(summary="Получить информацию о курсе", description="Возвращает информацию о курсе по его ID. Студенты видят только курсы, на которые они записаны.", tags=["Курсы"]),
    update=extend_schema(summary="Обновить курс", description="Обновляет данные курса по его ID. Доступно только преподавателям.", tags=["Курсы"]),
    partial_update=extend_schema(summary="Частично обновить курс", description="Частично обновляет данные курса по его ID. Доступно только преподавателям.", tags=["Курсы"]),
    destroy=extend_schema(summary="Удалить курс", description="Удаляет курс по его ID. Доступно только преподавателям.", tags=["Курсы"]),
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly, IsEnrolledOrTeacher]

    @extend_schema(summary="Записаться на курс", description="Позволяет студенту записаться на курс по его ID.", tags=["Курсы"])
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'status': 'enrolled'})

@extend_schema_view(
    list=extend_schema(summary="Получить список уроков", description="Возвращает список всех уроков. Студенты видят уроки только тех курсов, на которые они записаны.", tags=["Уроки"]),
    create=extend_schema(summary="Создать новый урок", description="Создает новый урок для курса. Доступно только преподавателям.", tags=["Уроки"]),
    retrieve=extend_schema(summary="Получить информацию об уроке", description="Возвращает информацию об уроке по его ID. Студенты видят уроки только тех курсов, на которые они записаны.", tags=["Уроки"]),
    update=extend_schema(summary="Обновить урок", description="Обновляет данные урока по его ID. Доступно только преподавателям.", tags=["Уроки"]),
    partial_update=extend_schema(summary="Частично обновить урок", description="Частично обновляет данные урока по его ID. Доступно только преподавателям.", tags=["Уроки"]),
    destroy=extend_schema(summary="Удалить урок", description="Удаляет урок по его ID. Доступно только преподавателям.", tags=["Уроки"]),
)
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrReadOnly]

@extend_schema_view(
    list=extend_schema(summary="Получить список заданий", description="Возвращает список всех заданий. Студенты видят задания только тех курсов, на которые они записаны.", tags=["Задания"]),
    create=extend_schema(summary="Создать новое задание", description="Создает новое задание для урока. Доступно только преподавателям.", tags=["Задания"]),
    retrieve=extend_schema(summary="Получить информацию о задании", description="Возвращает информацию о задании по его ID. Студенты видят задания только тех курсов, на которые они записаны.", tags=["Задания"]),
    update=extend_schema(summary="Обновить задание", description="Обновляет данные задания по его ID. Доступно только преподавателям.", tags=["Задания"]),
    partial_update=extend_schema(summary="Частично обновить задание", description="Частично обновляет данные задания по его ID. Доступно только преподавателям.", tags=["Задания"]),
    destroy=extend_schema(summary="Удалить задание", description="Удаляет задание по его ID. Доступно только преподавателям.", tags=["Задания"]),
)
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherOrReadOnly]



@extend_schema_view(
    list=extend_schema(summary="Получить список выполненных заданий", description="Возвращает список выполненных заданий. Студенты видят только свои задания, преподаватели — все.", tags=["Выполненные задания"]),
    create=extend_schema(summary="Отправить выполненное задание", description="Позволяет студенту отправить выполненное задание.", tags=["Выполненные задания"]),
    retrieve=extend_schema(summary="Получить информацию о выполненном задании", description="Возвращает информацию о выполненном задании по его ID. Студенты видят только свои задания.", tags=["Выполненные задания"]),
    update=extend_schema(summary="Обновить выполненное задание", description="Обновляет данные выполненного задания по его ID. Студенты могут редактировать только свои задания.", tags=["Выполненные задания"]),
    partial_update=extend_schema(summary="Частично обновить выполненное задание", description="Частично обновляет данные выполненного задания по его ID. Студенты могут редактировать только свои задания.", tags=["Выполненные задания"]),
    destroy=extend_schema(summary="Удалить выполненное задание", description="Удаляет выполненное задание по его ID. Студенты могут удалять только свои задания.", tags=["Выполненные задания"]),
)
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsOwnerOrTeacher]

    def get_queryset(self):
        if self.request.user.is_student:
            return Submission.objects.filter(student=self.request.user)
        return Submission.objects.all()

    def perform_create(self, serializer):
        # Автоматически устанавливаем student как текущего пользователя
        serializer.save(student=self.request.user)


@extend_schema_view(
    list=extend_schema(summary="Получить список отзывов", description="Возвращает список всех отзывов на курсы. Студенты видят отзывы только на курсы, на которые они записаны.", tags=["Отзывы"]),
    create=extend_schema(summary="Оставить отзыв на курс", description="Позволяет студенту оставить отзыв на курс, если он на него записан.", tags=["Отзывы"]),
    retrieve=extend_schema(summary="Получить информацию об отзыве", description="Возвращает информацию об отзыве по его ID.", tags=["Отзывы"]),
    update=extend_schema(summary="Обновить отзыв", description="Обновляет данные отзыва по его ID. Студенты могут редактировать только свои отзывы.", tags=["Отзывы"]),
    partial_update=extend_schema(summary="Частично обновить отзыв", description="Частично обновляет данные отзыва по его ID. Студенты могут редактировать только свои отзывы.", tags=["Отзывы"]),
    destroy=extend_schema(summary="Удалить отзыв", description="Удаляет отзыв по его ID. Студенты могут удалять только свои отзывы.", tags=["Отзывы"]),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrTeacher, CanReviewCourse]

    def get_queryset(self):
        if self.request.user.is_student:
            return Review.objects.filter(course__students=self.request.user)
        return Review.objects.all()