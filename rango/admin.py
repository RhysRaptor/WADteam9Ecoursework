from django.contrib import admin
from rango.models import UserProfile, Category, Meme

class MemeAdmin(admin.ModelAdmin) :
	list_display = ('title', 'category', 'image')

admin.site.register(Category)
admin.site.register(Meme, MemeAdmin)
admin.site.register(UserProfile)