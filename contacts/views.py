from rest_framework import generics, filters
from contacts.models import Contact
from contacts.serializers import ListContactSerializer, DetailContactSerializer
from contacts.permissions import IsOwner
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from contacts.forms import NewContactQuickForm, NewContactForm
from django.contrib import messages
from icecream import ic
from contacts.utils import make_new_contact_entry


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
    permission_classes = (IsOwner, )
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(owner=user)

@login_required
def contacts_index(request):
    context = {}
    contacts_list = Contact.objects.filter(owner__pk=request.user.pk)
    paginator = Paginator(contacts_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['new_contact_quick'] = NewContactQuickForm()
    return render(request, "contacts/index.html", context=context)


@login_required
def new_contact_quick_process(request):
    if request.method == "POST":
        form = NewContactQuickForm(request.POST)
        if form.is_valid():
            try:
                new_contact = Contact()
                new_contact.title = form.cleaned_data["title"]
                new_contact.phone_number = form.cleaned_data["phone_number"]
                new_contact.owner = request.user
                new_contact.save()
                messages.success(request, "مخاطب افزوده شد.")
            except Exception as error:
                ic(error)
                messages.error(request, "خطای رخ داده است. لطفا مجددا تلاش کنید.")
        else:
            ic(form.errors)
            messages.error(request, "خطا در پردازش فرم.")
    return redirect("contacts:index")


@login_required
def new_contact(request):
    context = {}
    context["form"] = NewContactForm()
    if request.method == "POST":
        form = NewContactForm(request.POST)
        if form.is_valid():
            contact_object = {
                "title" : form.cleaned_data["title"],
                "first_name" : form.cleaned_data["first_name"],
                "last_name" : form.cleaned_data["last_name"],
                "phone_number" : form.cleaned_data["phone_number"],
                "email" : form.cleaned_data["email"],
                "address" : form.cleaned_data["address"],
                "owner": request.user,
            }
            try:
                result = make_new_contact_entry(contact_object)
            except Exception as error:
                ic(error)
            if result["status"] == True:
                messages.success(request, "مخاطب افزوده شد.")
                return redirect("contacts:index")
        else:
            messages.error(request, "خطا در پردازش فرم.")
            ic(form.errors)
            return redirect("contacts:index")
    return render(request, "contacts/new_contact.html", context=context)


@login_required
def delete_contact(request):
    if request.method == "POST":
        item_to_delete = Contact.objects.get(pk=int(request.POST.get("id_to_delete")))
        try:
            if item_to_delete.owner.id == request.user.id:
                item_to_delete.delete()
                messages.info(request, "مخاطب حذف شد.")
        except Exception as error:
            ic(error)
            messages.error(request, "خطایی رخ داده است.")
    return redirect("contacts:index")         