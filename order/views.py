from rest_framework import viewsets, permissions, exceptions, status
from .serializers import *
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializers

    def get_queryset(self):
        """
        Return orders belonging to the authenticated user.
        Admin can view all orders.
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(buyer=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        order = serializer.save(buyer=self.request.user)

        return Response({"success": "Order created successfully.", "order_id": order.id},
                        status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status != 'awaiting_payment':
            raise ValidationError({"error": "The order has been processed and cannot be updated."})
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        return Response({"success": "Order updated successfully."},
                        status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        if instance.status != 'awaiting_payment':
            raise ValidationError({"error": "The order has been processed and cannot be deleted."})
        
        instance.delete()

        return Response({"succes": "Order deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
