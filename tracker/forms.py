from django import forms
from .models import Transaction, Category

class TransactionUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload Credit Card Statement (CSV)")

class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category']
