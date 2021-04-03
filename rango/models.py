from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
   
    def __str__(self):
        return self.user.username
   
   
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class Meme(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='memes')
    
    def __str__(self):
        return self.image