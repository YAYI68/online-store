

from rest_framework import exceptions as rest_exceptions
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


from inventory.models import Supplier, InventoryItem
from inventory.serializers import SupplierSerializer, SupplierDetailSerializer, InventoryItemSerializer, InventoryDetailItemSerializer
# Create your views here.


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
        try:
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
        except:
            raise rest_exceptions.ParseError('Supplier not found')

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            message = {
                "message": "Supplier deleted successfully"
            }
            return Response(message, status=status.HTTP_200_OK)
        except:
            raise rest_exceptions.ParseError('Supplier not found')


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
        try:
            inventory = InventoryItem.objects.get(pk=pk)
            serializer = InventoryDetailItemSerializer(inventory, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            raise rest_exceptions.ParseError('Inventory not found')

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

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            message = {
                "message": "Item deleted successfully"
            }
            return Response(message, status=status.HTTP_200_OK)
        except:
            raise rest_exceptions.ParseError('Inventory not found')
