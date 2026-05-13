from django.contrib import admin
from .models import LoanProduct

@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest_rate', 'max_tenure_years', 'min_income_required', 'max_dti_ratio')
    search_fields = ('name',)
