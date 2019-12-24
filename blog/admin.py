from django.contrib import admin
from blog import models


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
