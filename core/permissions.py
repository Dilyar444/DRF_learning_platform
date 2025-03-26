from rest_framework import permissions
from core.models import Course

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только преподаватели могут создавать, редактировать и удалять ресурсы.
    Студенты могут только просматривать (GET).
    """
    def has_permission(self, request, view):
        # Разрешить GET, HEAD, OPTIONS запросы всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить создание/изменение/удаление только преподавателям
        return request.user.is_authenticated and request.user.is_teacher

class IsOwnerOrTeacher(permissions.BasePermission):
    """
    Разрешение: студенты могут видеть только свои выполненные задания.
    Преподаватели могут видеть все выполненные задания.
    """
    def has_permission(self, request, view):
        # Преподаватели имеют полный доступ
        if request.user.is_authenticated and request.user.is_teacher:
            return True
        # Студенты могут видеть список своих заданий (для GET) или создавать новые (POST)
        return request.user.is_authenticated and request.user.is_student

    def has_object_permission(self, request, view, obj):
        # Преподаватели имеют полный доступ к любому объекту
        if request.user.is_teacher:
            return True
        # Студенты могут видеть/редактировать только свои выполненные задания
        return obj.student == request.user

class IsEnrolledOrTeacher(permissions.BasePermission):
    """
    Разрешение: студенты могут видеть курсы, только если они на них записаны.
    Преподаватели могут видеть все курсы.
    """
    def has_permission(self, request, view):
        # Преподаватели имеют полный доступ
        if request.user.is_authenticated and request.user.is_teacher:
            return True
        # Студенты могут видеть список курсов
        return request.user.is_authenticated and request.user.is_student

    def has_object_permission(self, request, view, obj):
        # Преподаватели имеют полный доступ
        if request.user.is_teacher:
            return True
        # Студенты могут видеть курс, только если они на него записаны
        return request.user in obj.students.all()
    
class CanReviewCourse(permissions.BasePermission):
    """
    Разрешение: студенты могут оставлять отзывы только на курсы, на которые они записаны.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            course_id = request.data.get('course')
            if not course_id:
                return False
            try:
                course = Course.objects.get(id=course_id)
                return request.user in course.students.all()
            except Course.DoesNotExist:
                return False
        return True