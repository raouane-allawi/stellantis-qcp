from django.contrib import admin
from .models import Zone, KPIRecord, KPIConfig, AuditLog

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    filter_horizontal = ['users']

@admin.register(KPIRecord)
class KPIRecordAdmin(admin.ModelAdmin):
    list_display = ['value', 'rsp', 'zone', 'datetime_extraction', 'source']
    list_filter = ['rsp', 'zone', 'source']

@admin.register(KPIConfig)
class KPIConfigAdmin(admin.ModelAdmin):
    list_display = ['zone', 'kpi_type', 'target_value', 'alert_threshold', 'unit']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'timestamp']
    list_filter = ['action']
    readonly_fields = ['user', 'action', 'description', 'ip_address', 'timestamp']