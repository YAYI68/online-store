
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers, exceptions as jwt_exceptions
from django.template.loader import render_to_string
from inventory.models import Supplier, InventoryItem


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryItem
        fields = ("id", "name", "price", "quantity")


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ("id", "name", "email", "phone_number", "address")


class SupplierDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Supplier
        fields = ("id", "name", "email", "phone_number", "address", "items")

    def get_items(self, obj):
        serializer = ItemSerializer(obj.items, many=True)
        return serializer.data


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
