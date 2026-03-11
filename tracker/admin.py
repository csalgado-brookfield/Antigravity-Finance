from django.contrib import admin
from .models import Category, Transaction, Account, MerchantEnrichment

@admin.register(MerchantEnrichment)
class MerchantEnrichmentAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'clean_name', 'category', 'user')
    list_filter = ('category', 'user')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_four', 'user')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_budget', 'color')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'category', 'account', 'user')
    list_filter = ('category', 'account', 'date', 'user')
    search_fields = ('description',)
