from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status, mixins
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from repair_service.models import Invoice, Request
from repair_service.permissions import IsAdminOrIfAuthenticatedReadOnly
from repair_service.serializers import InvoiceSerializer, RequestSerializer, MasterRequestSerializer, \
    RequestListSerializer


class Pagination(PageNumberPagination):
    page_size = 10


class InvoiceViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = Pagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return Invoice.objects.all()
        return Invoice.objects.filter(request__user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.paid:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RequestViewSet(viewsets.ModelViewSet):

    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = Pagination

    def get_queryset(self):

        user = self.request.query_params.get("user")
        phone_model = self.request.query_params.get("phone_model")
        problem_description = self.request.query_params.get("problem_description")

        queryset = self.queryset

        if phone_model:
            queryset = queryset.filter(phone_model__icontains=phone_model)

        if problem_description:
            queryset = queryset.filter(problem_description__icontains=problem_description)

        if self.request.user.is_staff:
            if user:
                queryset = queryset.filter(user_id__in=user)

            return queryset.distinct()

        return queryset.filter(user=self.request.user).distinct()

    def get_serializer_class(self):

        if self.action in ["update", 'partial_update']:
            if self.request.user.is_staff:
                return MasterRequestSerializer
            return RequestSerializer

        if self.action in ["list", "retrieve"]:
            return RequestListSerializer

        return RequestSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "In line":
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user",
                type=OpenApiTypes.INT,
                description="Filter by user id (ex. ?user=2)",
            ),
            OpenApiParameter(
                "phone_model",
                type=OpenApiTypes.STR,
                description="Filter by phone_model (ex. ?phone_model='phonename')",
            ),
            OpenApiParameter(
                "phone_description",
                type=OpenApiTypes.STR,
                description="Filter by phone_description (ex. ?phone_description='phonedescription')",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
