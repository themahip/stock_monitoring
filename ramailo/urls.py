from django.conf.urls import include
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from ramailo.views import health
from ramailo.views.feedback import feedback, raise_ticket
from ramailo.views.notification import set_fcm_device
from ramailo.views.onboarding import LoginView, OtpView, logout
from ramailo.views.user import ProfileView
from ramailo.views.kyc import set_email, verify_email

from .openapi_info import openapi_info


def trigger_error(request):
    division_by_zero = 1 / 0


class OptionalSlashRouter(DefaultRouter):
    def __init__(self):
        super(DefaultRouter, self).__init__()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()

schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

utils_paths = [
    re_path('^', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('health/', health, name='health'),
    path('sentry-debug/', trigger_error),
]

api_paths = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('otp/', OtpView.as_view(), name='token_view'),
    path('login/', LoginView.as_view(), name='token_obtain_view'),
    path('logout/', logout, name='logout'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Kyc
    path('email/', set_email, name='set link email'),
    path('kyc/email/validate/<token>/', verify_email, name='verify link email'),

    # feedbacks
    path('feedback/', feedback, name='user_feedback'),
    path('ticket/', raise_ticket, name='raise_ticket'),

    # fcm device
    path('fcm/register/', set_fcm_device, name='register_fcm_device'),

]

urlpatterns = utils_paths + api_paths
