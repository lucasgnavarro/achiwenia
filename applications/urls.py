from django.urls import path
from .views import ApplicationView


urlpatterns = [
    path('', ApplicationView.as_view(), name='applications_applications'),

    # path('login/', LoginView.as_view(), name='userccounts_login'),
    # path('login/<uuid:app_id>/', LoginView.as_view(), name='userccounts_login'),
    # path('register/', RegisterView.as_view(), name='userccounts_register'),
    # path('register/<uuid:app_id>/', RegisterView.as_view(), name='userccounts_register'),
]
