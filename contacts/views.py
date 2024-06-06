from rest_framework import generics, filters
from contacts.models import Contact
from contacts.serializers import ListContactSerializer, DetailContactSerializer
from contacts.permissions import IsOwner
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from contacts.forms import NewContactQuickForm, NewContactForm
from django.contrib import messages
from icecream import ic
from contacts.utils import make_new_contact_entry
from django.http import HttpResponseForbidden
import csv


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
    contacts_list = Contact.objects.filter(owner__pk=request.user.pk).order_by("date_created")
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


@login_required
def edit_contact(request):
    # view to get and display the edit form
    context = {}
    if request.method == "POST":
        item_to_edit = Contact.objects.get(pk=int(request.POST.get("id_to_edit")))
        data = {}
        data["title"] = item_to_edit.title
        data["first_name"] = item_to_edit.first_name
        data["last_name"] = item_to_edit.last_name
        data["phone_number"] = item_to_edit.phone_number
        data["email"] = item_to_edit.email
        data["address"] = item_to_edit.address
        form = NewContactForm(data=data)
        context["form"] = form
        context["full_name"] = item_to_edit.full_name
        context["item_id"] = item_to_edit.id
    else:
        return HttpResponse("مخاطبی برای ویرایش یافت نشد.")
    return render(request, "contacts/edit_contact.html", context=context)

@login_required
def edit_contact_process(request):
    if request.method == "POST":
        try:
            form = NewContactForm(request.POST)
        except Exception as form_error:
            ic(form_error)
            messages.error(request, "خطا سیستم")
            return redirect("contacts:index")
        if form.is_valid():
            try:
                item = Contact.objects.get(pk=int(request.POST.get("item_id")))
            except Exception as item_retrieve_error:
                ic(item_retrieve_error)
                return redirect("contacts:index")
            try:
                if item.owner.id != request.user.id:
                    return HttpResponseForbidden()
            except Exception as resource_error:
                ic(resource_error)
                return HttpResponseForbidden()
            try:
                item.title = form.cleaned_data["title"]
                item.first_name = form.cleaned_data["first_name"]
                item.last_name = form.cleaned_data["last_name"]
                item.phone_number = form.cleaned_data["phone_number"]
                item.email = form.cleaned_data["email"]
                item.address = form.cleaned_data["address"]
            except Exception as data_update_error:
                ic(data_update_error)
                messages.error("خطای سیستم.")
            try:
                item.save()
                messages.success(request, "ویرایش با موفقیت انجام شد.")
                return redirect("contacts:index")
            except Exception as update_process_error:
                ic(update_process_error)
                return redirect("contacts:index")
    return redirect("contacts:index")


@login_required
def download_csv(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get("id_for_csv")
            if request.user.id != int(user_id):
                return HttpResponseForbidden()
        except Exception as error:
            messages.error(request, "این اقدام در حال حاضر امکان پذیر نیست.")
            return redirect("contacts:index")
        try:
            user_item_list = Contact.objects.filter(owner__pk=request.user.pk)
        except Exception as error:
            messages.error(request, "خطا در پردازش درخواست.")
            return redirect("contacts:index")
        try: 
            response = HttpResponse(
                    content_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="{username}_contacts.csv"'.format(username=request.user.username)},)
            writer = csv.writer(response)
            writer.writerow(["title", "first_name", "last_name", "phone_number", "email", "address", "date_created", "last_modified"])
            for item in user_item_list:
                writer.writerow([item.title, item.first_name, item.last_name, item.email, item.address, item.date_created, item.last_modified])
                return response
        except Exception as error:
            messages.error(request, "خطا در پردازش درخواست.")
    return redirect("contacts:index")