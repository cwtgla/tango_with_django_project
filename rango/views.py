from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

#helper method
def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

#updated function definition
def visitor_cookie_handler(request):
	#get the number of visits tot he site
	#use cookies.get() function to obtain the visits cookie
	#if it exists the value returned is casted to an integer
	#if the cookie doesnt exist the default value of 1 is used
	visits = int(get_server_side_cookie(request,'visits','1'))

	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

	#if its been more than a day since the last visit
	if(datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		#update the last visit cookie now that we have updated the count
		request.session['last_visit'] = str(datetime.now())
	else:
		visits = 1
		#set the last visit cookie
		request.session['last_visit'] = last_visit_cookie

	#uodate set the visits cookie
	request.session['visits'] = visits

def index(request):
	request.session.set_test_cookie()
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories':category_list, 'pages':page_list}

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	response = render(request, 'rango/index.html', context=context_dict)

	return response

#use login_required() decorator to ensure only logged in users can access this
@login_required
def user_logout(request):
	#since we knew the user is logged in we can just log them out
	logout(request)
	#redirect o homepage
	return HttpResponseRedirect(reverse('index'))

def register(request):
	#A bool flag telling the template whether reg was successful, false initially
	registered = False

	#if http post we want to try process data
	if request.method == 'POST':
		#try grab info from raw form info (user and userprofileform)
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#if both forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			#save users form data to db
			user = user_form.save()

			#now hash the password with set_password method and update object
			user.set_password(user.password)
			user.save()

			#now sort out userprofile isntance
			#need to set user attribute ourselves
			#set commit=false, this delays saving the model
			#until we're ready
			profile = profile_form.save(commit=False)
			profile.user = user

			#did the user give ap rofile pic? if so
			#we need to get it from the form and put
			#it in the UserProfile model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			#now save the userpropfile model instance
			profile.save()

			#update our variable to indiciate that the template
			#registration was successful
			registered = True
		else:
			#invalid form or forms, mistakes etc? print errors to terminal
			print(user_form.errors, profile_form.errors)
	else:
		#not a http post so we render our form using two modelform instances
		#these forms will be blank, ready for user input
		user_form = UserForm()
		profile_form = UserProfileForm()

	#render the templat depending ont he context
	return render(request, 'rango/register.html', {'user_form': user_form,
												   'profile_form': profile_form,
												   'registered':registered})


def about(request):
	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()

	visitor_cookie_handler(request)
	context_dict = {}
	context_dict['visits'] = request.session['visits']

	return render(request, 'rango/about.html', context=context_dict)

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})

def user_login(request):
	#if request is a http post try get relevant info
	if request.method == 'POST':
		#get username and password
		#from login form, using post.get([var])
		#we get none rather than key var for error handling
		username = request.POST.get('username')
		password = request.POST.get('password')

		#use djangos machinery to see if username/password combo is valid
		#user object is returned if it is
		user = authenticate(username=username, password=password)

		#if we get user object the details are correct
		if user:
			#is account active? could be disabled
			if user.is_active:
				#log user in and redirect
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			#bad login details were provided
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		#HTTP GET so send to login form
		return render(request, 'rango/login.html', {})

def show_category(request, category_name_slug):
	#create context dict prior to passing it to the template rendering engine
	context_dict = {}

	try:
		#attempt to find a category name slug with the given name
		#get returns an exception or a model instance so need excep handling at the bottom
		category = Category.objects.get(slug=category_name_slug)

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

@login_required
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	context_dict = {'form':form, 'category':category}
	return render(request, 'rango/add_page.html', context_dict)

@login_required
def add_category(request):
	form = CategoryForm()

	#http post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#have we been provided a valid form?
		if form.is_valid():
			form.save(commit=True)
			#now that category is saved we could give confirmation message
			#but since most recent category is added on index page we can redirect there
			return index(request)
		else:
			#supplied form has errors, print them to terminal
			return(form.errors)
	#will handle the bad form, new form or no form supplied
	return render(request, 'rango/add_category.html', {'form': form})
