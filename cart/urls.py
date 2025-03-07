from django.urls import path
from cart.api.views import CartViewSet

urlpatterns = [
    path('update_item/<int:item_id>/', CartViewSet.as_view({'put': 'update_item'}), name='update_item')
]
