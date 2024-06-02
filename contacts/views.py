from rest_framework import generics
from contacts.models import Contact
from contacts.serializers import ListContactSerializer, DetailContactSerializer
# from contacts.permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters

class ContactsList(generics.ListCreateAPIView):
    serializer_class = ListContactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailContactSerializer
    # permission_classes = (IsOwner, )

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(owner=user)