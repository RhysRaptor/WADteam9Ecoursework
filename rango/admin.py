from django.contrib import admin
from rango.models import UserProfile, Category, Meme

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

class MemeAdmin(admin.ModelAdmin) :
	prepopulated_fields = {'slug':('title',)}
	list_display = ('title', 'category', 'image')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Meme, MemeAdmin)
admin.site.register(UserProfile)