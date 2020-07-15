from rest_framework import serializers

from . import models


class DoubtSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Doubt
        fields = ('id', 'question', 'question_type')
        read_only_fields = ('id',)
        write_only_fields = ('user',)
