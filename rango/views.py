from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page


def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:6]
	context_dict = {'categories':category_list}

	return render(request, 'rango/index.html', context_dict)

def about(request):
	return render(request, 'rango/about.html')

def show_category(request, category_slug_name):
	#create context dict prior to passing it to the template rendering engine
	context_dict = {}

	try:
		#attempt to find a category name slug with the given name
		#get90 returns an exception or a model instance so need excep handling at the bottom
		category = Category.objects.get(slug=category_slug_name)

		#get all relevant pages, filter returns a list either with elements or empty
		pages = Page.objects.filter(category=category)

		#add results pages to our context dictionary
		context_dict['pages'] = pages

		#also add category object to context to verify category exists
		context_dict['category'] = category
	except Category.DoesNotExist:
		#no category exists for url so do nothing
		context_dict['category'] = None
		context_dict['pages'] = None

	return render(request, 'rango/category.html', context_dict)