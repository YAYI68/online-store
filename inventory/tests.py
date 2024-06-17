from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from inventory.models import Supplier, InventoryItem
from user.models import User  # Assuming you have a User model for authentication


class InventoryViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Creating a test user and authenticating
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.client.login(email='testuser@example.com', password='password123')

        self.supplier_data = {
            'name': 'Test Supplier',
            'phone_number': '1234567890',
            'address': 'Test Address'
        }

        self.inventory_item_data = {
            'name': 'Test Item',
            'price': 100.0,
            'quantity': 10,
        }

        self.supplier = Supplier.objects.create(**self.supplier_data)
        self.inventory_item_data['supplier'] = self.supplier.id
        self.inventory_item = InventoryItem.objects.create(
            **self.inventory_item_data)

        # Add the correct URL name for supplier list/create
        self.supplier_url = reverse('supplier-list-create')
        # Add the correct URL name for supplier detail
        self.supplier_detail_url = reverse(
            'supplier-detail-update-delete', kwargs={'pk': self.supplier.id})
        # Add the correct URL name for inventory list/create
        self.inventory_url = reverse('inventory-list-create')
        self.inventory_detail_url = reverse('inventory-detail-update-delete', kwargs={
                                            'pk': self.inventory_item.id})  # Add the correct URL name for inventory detail

    def test_supplier_creation(self):
        response = self.client.post(
            self.supplier_url, data=self.supplier_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 2)

    def test_supplier_listing(self):
        response = self.client.get(self.supplier_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_supplier_detail_retrieval(self):
        response = self.client.get(self.supplier_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.supplier_data['name'])

    def test_supplier_update(self):
        updated_data = {'name': 'Updated Supplier'}
        response = self.client.patch(
            self.supplier_detail_url, data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, updated_data['name'])

    def test_supplier_deletion(self):
        response = self.client.delete(self.supplier_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Supplier.objects.count(), 0)

    def test_inventory_item_creation(self):
        response = self.client.post(
            self.inventory_url, data=self.inventory_item_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 2)

    def test_inventory_item_listing(self):
        response = self.client.get(self.inventory_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_inventory_item_detail_retrieval(self):
        response = self.client.get(self.inventory_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'],
                         self.inventory_item_data['name'])

    def test_inventory_item_update(self):
        updated_data = {'name': 'Updated Item'}
        response = self.client.patch(
            self.inventory_detail_url, data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory_item.refresh_from_db()
        self.assertEqual(self.inventory_item.name, updated_data['name'])

    def test_inventory_item_deletion(self):
        response = self.client.delete(self.inventory_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InventoryItem.objects.count(), 0)
