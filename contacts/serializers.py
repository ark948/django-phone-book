from rest_framework import serializers
from contacts.models import Contact

class ListContactSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    details = serializers.HyperlinkedIdentityField(view_name='contacts:contact-detail')

    class Meta:
        model = Contact
        fields = ["title", "full_name", "owner", 'details']

class DetailContactSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Contact
        fields = "__all__"