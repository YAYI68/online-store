
from user.models import User
from rest_framework import serializers


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserSeriliazer(serializers.ModelSerializer):
    firstname = serializers.CharField(source='first_name')
    lastname = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname')
