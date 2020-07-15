from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'account_type', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password', code='authentication')
        data['user'] = user
        return data
