from django.contrib import admin

from ramailo.models.feedback import Feedback
from ramailo.models.notification import FCMDevice
from ramailo.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'idx', 'mobile', 'name', 'position', 'created_at']
    search_fields = ['name', 'mobile']
    list_filter = ['is_approved', 'is_email_verified', 'is_kyc_verified']


admin.site.register(FCMDevice)