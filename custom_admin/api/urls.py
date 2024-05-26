from django.urls import path
from rest_framework import routers

from custom_admin.api import views
from custom_admin.utils.register_admin_viewsets import register_admin_viewsets

admin_router = routers.SimpleRouter()

register_admin_viewsets(admin_router)

urlpatterns = [
    path('autocompete/<str:app_label>/<str:model_name>/', views.AutoCompeteView.as_view()),
    path('token-auth/', views.AdminAuthToken.as_view()),

    path(
        'get_sections/',
        views.GetAdminSectionsAPIView.as_view(router=admin_router),
        name='get-sections',
    ),
]

urlpatterns += admin_router.urls
