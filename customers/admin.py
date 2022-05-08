from django.contrib import admin
from .models import Customer, Address, Bank
# Register your models here.


class AddressInline(admin.TabularInline):
    model = Address
    verbose_name_plural = 'Address'
    extra = 0

class BankInline(admin.TabularInline):
    model = Bank
    verbose_name_plural = 'Bank'
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'phone',  'email']
	search_fields = ('first_name', 'last_name', 'phone',  'email')
	inlines = [AddressInline, BankInline]

	class Meta:
		model = Customer


admin.site.register(Customer, CustomerAdmin)