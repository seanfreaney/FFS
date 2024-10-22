from django.contrib import admin
from .models import ServiceRequest, Document

# Register your models here.
admin.site.register(ServiceRequest)

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1
    fields = ('file', 'is_bank_statement', 'is_completed_file', 'uploaded_by')
    readonly_fields = ('uploaded_at',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If this is a new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['service_request', 'file', 'uploaded_at', 'uploaded_by']
    list_filter = ['uploaded_at', 'uploaded_by']
    search_fields = ['service_request__request_number', 'file']
    readonly_fields = ('uploaded_at',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If this is a new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'file':
            formfield.help_text = 'Allowed file types: Excel (.xlsx, .xls), PDF (.pdf), Images (.jpg, .jpeg, .png)'
        return formfield
