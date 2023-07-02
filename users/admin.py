from django.contrib import admin

# Register your models here.
from products.admin import BasketAdmin
from users.models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)

@admin.register(EmailVerification )
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expired')
    fields = ('code', 'user', 'expired', 'created')
    readonly_fields = ('created',)