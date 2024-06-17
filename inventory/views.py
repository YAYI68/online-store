
from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions as rest_exceptions
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from decouple import config
from django.http import JsonResponse


from inventory.models import User, Supplier, InventoryItem
from inventory.serializers import UserSignUpSerializer, UserSeriliazer, SupplierSerializer, SupplierDetailSerializer, InventoryItemSerializer, InventoryDetailItemSerializer
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


class SupplierView(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        serializer = SupplierDetailSerializer(supplier, many=False)
        return Response(serializer.data)

    def patch(self, request, pk):
        data = request.data
        supplier = Supplier.objects.get(pk=pk)
        if supplier is None:
            raise rest_exceptions.NotFound(detail="Supplier not found.")

        dataObj = {
            "name": data.get("name", supplier.name),
            # "email": data.get("email", supplier.email),
            "phone_number": data.get("phone_number", supplier.phone_number),
            "address": data.get("address", supplier.address),
        }
        serializer = SupplierSerializer(
            supplier, data=dataObj, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = InventoryItemSerializer
    queryset = InventoryItem.objects.all()
    permission_classes = [IsAuthenticated]


def post(self, request):
    data = request.data
    serializer = InventoryItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryItemSerializer
    queryset = InventoryItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        inventory = InventoryItem.objects.get(pk=pk)
        serializer = InventoryDetailItemSerializer(inventory, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            data = request.data
            item = InventoryItem.objects.get(pk=pk)
            if item is None:
                raise rest_exceptions.NotFound(detail="Item not found.")
            dataObj = {
                "name": data.get("name", item.name),
                "price": data.get("price", item.price),
                "quantity": data.get("quantity", item.quantity),
                "supplier": data.get("supplier", item.supplier),
            }

            serializer = InventoryItemSerializer(
                item, data=dataObj, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            raise rest_exceptions.ParseError('Inventory not found')
