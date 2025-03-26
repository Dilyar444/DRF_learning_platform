from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt  # Импортируем csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.utils import extend_schema
from core import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'submissions', views.SubmissionViewSet)
router.register(r'reviews', views.ReviewViewSet)

# Декорируем obtain_auth_token для Swagger и отключаем CSRF
@extend_schema(
    summary="Получить токен аутентификации",
    description="Возвращает токен для аутентификации пользователя. Требуется передать username и password.",
    tags=["Аутентификация"],
    responses={
        200: {
            "type": "object",
            "properties": {
                "token": {"type": "string", "description": "Токен аутентификации"}
            }
        }
    }
)
@csrf_exempt  # Отключаем CSRF-проверку
def decorated_obtain_auth_token(request):
    return obtain_auth_token(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', decorated_obtain_auth_token, name='api_token_auth'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)