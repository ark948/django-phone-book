from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def index(request):
    return Response({
        "contacts": reverse("contacts:contacts-list", request=request),
        "accounts": reverse("accounts:user-list", request=request),
    })