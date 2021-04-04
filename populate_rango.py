import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
					  'rate_my_meme_coursework.settings')
import django
django.setup()
from rango.models import Category, Meme 

def populate():
	video_games_memes = [
		{'title': 'wanda_thanos_endgame',
		'image' : 'wanda_thanos_endgame.jpg'},
		{'title': 'mandalorian_getting_carried',
		'image' : 'mandalorian_getting_carried.jpg'},
		{'title': 'incredibles_coincidence',
		'image' : 'incredibles_coincidence.jpg'}]

	spongebob_memes = [
		{'title': 'spongebob_exam',
		'image' : 'spongebob_exam.jpg'},
		{'title': 'spongebob_microwave',
		'image' : 'spongebob_microwave.jpg'},
		{'title': 'spongebob_shellphone',
		'image' : 'spongebob_shellphone.jpg'}]

	cats = {'Video Games': {'memes' : video_games_memes},
			'Spongebob': {'memes': spongebob_memes}}

	for cat, cat_data in cats.items():
		c = add_cat(cat)
		for p in cat_data['memes']:
			add_page(c, p['title'], p['image'])

	for c in Category.objects.all():
		for p in Meme.objects.filter(category=c):
			print(f'- {c}: {p}')

def add_page(cat, title, image, views=0):
	p = Meme.objects.get_or_create(category=cat, title=title)[0]
	p.image=image
	p.save()
	return p

def add_cat(name):
	c = Category.objects.get_or_create(name=name)[0]
	c.save()
	return c

if __name__ == '__main__':
	print('Starting Rango population script...')
	populate()