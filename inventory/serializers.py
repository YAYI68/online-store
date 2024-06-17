
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers, exceptions as jwt_exceptions
from django.template.loader import render_to_string
from inventory.models import User, Supplier, InventoryItem


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserSeriliazer(serializers.ModelSerializer):
    firstname = serializers.CharField(source='first_name')
    lastname = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname')


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ("id", "name", "email", "phone_number", "address")


class SupplierDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ("id", "name", "email", "phone_number", "address", "items")

    def get_items(self, obj):
        return obj.items


class InventoryItemSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all())

    class Meta:
        model = InventoryItem
        fields = ("id", "name", "price", "quantity", "supplier")


class InventoryDetailItemSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'price', 'quantity', 'supplier']
