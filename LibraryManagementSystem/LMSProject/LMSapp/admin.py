
from django.contrib import admin
from django.apps import apps

from .forms import BookCreateForm
from .models import *
class BookCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'book_name', 'quantity','issue_by']
   form = BookCreateForm
   list_filter = ['category']
   search_fields = ['category', 'book_name']

admin.site.register(Book,BookCreateAdmin)
admin.site.register(Category)

class ModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)

models = apps.get_models()
for model in models:
    try:
        admin.site.register(model,ModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass