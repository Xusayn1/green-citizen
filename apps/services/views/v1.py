from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.services.serializers.list import ServiceTypeListSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.services.models import ServiceType

class ServiceTypeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceTypeListSerializer


    def get(self, request):
        services = ServiceType.objects.all()
        serializer = self.serializer_class(services, many=True, context={'request': request})
        return CustomResponse.success(request=request, data=serializer.data)


    def post(self,  request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return CustomResponse.validation_error(request=request, errors=serializer.errors)
        service = serializer.save()
        return CustomResponse.success(request=request, data=self.serializer_class(service, context={'request': request}).data)


    def delete(self, request, id):
        service = ServiceType.objects.get(id=id)
        service.soft_delete()
        return CustomResponse.success(request=request, message_key="SERVICE_DELETED")


    def put(self, request, id):
        service = ServiceType.objects.get(id=id)
        serializer = self.serializer_class(service, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return CustomResponse.validation_error(request=request, errors=serializer.errors)
        service.save()
        return CustomResponse.success(request=request, data=self.serializer_class(service, context={'request': request}).data)

    def patch(self, request, id):
        service = ServiceType.objects.get(id=id)
        serializer = self.serializer_class(service, data=request.data, context={'request': request}, partial=True)
        if not serializer.is_valid():
            return CustomResponse.validation_error(request=request, errors=serializer.errors)
        service.save()
        return CustomResponse.success(request=request, data=self.serializer_class(service, context={'request': request}).data)

    def partial_update(self, request, id):
        service = ServiceType.objects.get(id=id)
        serializer = self.serializer_class(service, data=request.data, context={'request': request}, partial=True)
        if not serializer.is_valid():
            return CustomResponse.validation_error(request=request, errors=serializer.errors)
        service.save()
        return CustomResponse.success(request=request, data=self.serializer_class(service, context={'request': request}).data)
