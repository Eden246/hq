from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_menuitems_count', 'related_menuitems_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                MenuItem,
                'category',
                'menuitems_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 MenuItem,
                 'category',
                 'menuitems_count',
                 cumulative=False)
        return qs

    def related_menuitems_count(self, instance):
        return instance.menuitems_count
    related_menuitems_count.short_description = 'Related menuitems (for this specific category)'

    def related_menuitems_cumulative_count(self, instance):
        return instance.menuitems_cumulative_count
    related_menuitems_cumulative_count.short_description = 'Related menuitems (in tree)'

admin.site.register(MenuItem)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OrderModel)
admin.site.register(OrderItem)