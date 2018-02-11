from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary
	# that will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories':category_list}

	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list

	return render(request, 'rango/index.html', context_dict)

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
	return render(request, 'rango/about.html')

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
