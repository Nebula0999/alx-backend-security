from django.contrib import admin
from .models import RequestLog, BlockedIP


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'timestamp', 'country', 'city')
    list_filter = ('timestamp', 'country', 'city')
    search_fields = ('ip_address', 'path', 'country', 'city')
    ordering = ('-timestamp',)

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocked_at')
    search_fields = ('ip_address',)
    ordering = ('-blocked_at',)

# Register your models here.
