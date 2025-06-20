from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        """
        Validate data.

        :param data: Data for the user.
        :return: Validated data.
        :raises: ValidationError.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": " ".join(e)})

        return data

    def create(self, validated_data):
        """
        Create a new user.

        :param validated_data: Validated data for the user.
        :return: Created user instance.
        """

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user