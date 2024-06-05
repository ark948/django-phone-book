from django import forms

class NewContactQuickForm(forms.Form):
    title = forms.CharField(max_length=200, label="عنوان:", required=True)
    phone_number = forms.CharField(max_length=150, label="شماره تماس:", required=False)