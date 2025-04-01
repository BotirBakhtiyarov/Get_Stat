from django.contrib import admin
from .models import Computer, AppUsage, SystemMetrics

class AppUsageInline(admin.TabularInline):
    model = AppUsage
    extra = 0

class SystemMetricsInline(admin.TabularInline):
    model = SystemMetrics
    extra = 0

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('computer_id', 'username', 'last_seen')
    search_fields = ('computer_id', 'username')
    inlines = [AppUsageInline, SystemMetricsInline]

@admin.register(AppUsage)
class AppUsageAdmin(admin.ModelAdmin):
    list_display = ('computer', 'app_name', 'duration', 'cpu_usage', 'ram_usage')
    list_filter = ('app_name',)

@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ('computer', 'cpu_percent', 'ram_percent', 'timestamp')
    list_filter = ('timestamp',)