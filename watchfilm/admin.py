from django.contrib import admin
from .model import Film, kmean_recom, user

# Register your models here.
class filmAdmin(admin.ModelAdmin):
	list_display = ("title", 'category', 'rating', 'image_url')


admin.site.register(Film, filmAdmin)
admin.site.register(kmean_recom)
admin.site.register(user)