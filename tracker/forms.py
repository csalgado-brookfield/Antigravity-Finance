from django import forms
from .models import Transaction, Category, Account

class TransactionUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload Credit Card Statement (CSV)")
    account = forms.ModelChoiceField(queryset=Account.objects.none(), required=False, label="Select Account (Optional)")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)

class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category']
