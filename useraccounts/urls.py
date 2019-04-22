from django.urls import path

from .views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='userccounts_index'),

    # path('login/', LoginView.as_view(), name='userccounts_login'),
    # path('login/<uuid:app_id>/', LoginView.as_view(), name='userccounts_login'),
    # path('register/', RegisterView.as_view(), name='userccounts_register'),
    # path('register/<uuid:app_id>/', RegisterView.as_view(), name='userccounts_register'),
]
