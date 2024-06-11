from django.contrib import admin
from .models import Recipe, RecipeCategory
# Register your models here.

admin.site.register(Recipe)
admin.site.register(RecipeCategory)
