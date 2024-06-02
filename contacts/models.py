from django.db import models
from accounts.models import CustomUser
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Contact(models.Model):
    title = models.CharField("Title", null=False, blank=False, max_length=200)
    first_name = models.CharField("First Name", null=True, blank=True, max_length=100)
    last_name = models.CharField("Last Name", null=True, blank=True, max_length=150)
    phone_number = models.CharField("Phone/Cell Number", null=True, blank=True, max_length=40)
    email = models.EmailField("Email Address", null=True, blank=True)
    address = models.TextField("Address", null=True, blank=True)
    date_created = models.DateTimeField("Created on", auto_now_add=True)
    last_modified = models.DateField("Modified on", auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return f"<Contact for {self.owner} - ID:{self.id}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse("contact_api:contact_detail", kwargs={"pk": self.pk})