
from django.urls import path, re_path
from inventory.views import logout, UserRegistrationView, LoginView, SupplierView, SupplierUpdateDeleteView, InventoryView, InventoryDetailUpdateDeleteView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('supplier/', SupplierView.as_view()),
    path('inventory/', InventoryView.as_view()),
    path('supplier/<str:pk>/', SupplierUpdateDeleteView.as_view()),
    path('inventory/<str:pk>/', InventoryDetailUpdateDeleteView.as_view()),

    #  not found route

]
