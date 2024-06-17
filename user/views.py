from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions as rest_exceptions
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


from user.models import User
from user.serializers import UserSignUpSerializer, UserSeriliazer
# Create your views here.


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            data = get_tokens_for_user(user)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=data["access_token"],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=data["refresh_token"],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            csrf.get_token(request)
            userInfo = UserSeriliazer(user).data
            response.data = {"success": "Login successfully",
                             'access_token': data['access_token'], 'refresh_token': data['refresh_token'], 'user': userInfo}
            response.status = status.HTTP_200_OK
            response['X-CSRFToken'] = csrf.get_token(request)
            return response
        raise rest_exceptions.AuthenticationFailed(
            'Invalid Email or password!!'
        )


@api_view(['POST'])
def logout(request):
    try:
        refresh = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = RefreshToken(refresh)
        token.blacklist()
        res = Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie('X-CSRFToken')
        res.delete_cookie('csrftoken')
        return res
    except:
        raise rest_exceptions.ParseError('Invalid Token')
