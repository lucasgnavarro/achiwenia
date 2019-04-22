from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .serializers import UserRoleSerializer
from .models import UserRole


class IndexView(views.APIView):

    def get(self, request):
        user_roles = UserRole.objects.all()
        to_response = UserRoleSerializer(user_roles, many=True)
        return Response(to_response.data)


class LoginView(views.APIView):

    def post(self, request):
            pass


