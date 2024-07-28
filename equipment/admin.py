from django.contrib import admin
from .models import Equipment, MovementHistory


class MovementHistoryInline(admin.TabularInline):
    """История перемещения"""
    model = MovementHistory
    extra = 0  # сколько пустых отзывов отображать
    readonly_fields = ('created',)  # Делаем поле времени для отображения и только для чтения


class EquipmentAdmin(admin.ModelAdmin):
    inlines = [
        MovementHistoryInline
    ]
    list_display = (
        'title',
        'manufacturer',
        'inventory_number',
        'serial_number',
        'department',
        'bar_number',
    )


admin.site.register(Equipment, EquipmentAdmin)
