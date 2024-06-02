from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    contacts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='contacts:contact-detail'
    )
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "contacts")