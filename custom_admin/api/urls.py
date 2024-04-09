from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token

from custom_admin.api import views
from custom_admin.utils.register_admin_viewsets import register_admin_viewsets

admin_router = routers.SimpleRouter()

register_admin_viewsets(admin_router)

urlpatterns = [
    path('autocompete/', views.AutoCompeteView.as_view()),
    path('token-auth/', views.AdminAuthToken.as_view()),
    path('change-language/', views.ChangeLanguageAPIView.as_view(), name='change-language'),
    path('token-refresh/', refresh_jwt_token),

    path(
        'get_sections/',
        views.GetAdminSectionsAPIView.as_view(router=admin_router),
        name='get-sections',
    ),
]

urlpatterns += admin_router.urls
