from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from . import models


class DoubtViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DoubtSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Doubt.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.order_by('-question_type')

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if self.action == 'list':
            if request.user.account_type == 'teacher':
                return response
            else:
                response.data = []
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
        return response
