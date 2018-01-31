import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django

django.setup()

from rango.models import Category, Page


def populate():
    # Creating a list of dictionaries containing pages we want to add to each category
    # Then a dictionary of dictionaries for our categories
    # Allows us to iterate through data structures to add data to our models?

    # Cats dict contains "CATEGORY" : {"PAGES" : CATEGORY_PAGES}
    # category : dict so dict of dicts?
    python_pages = [{"title": "Official Python Tutorial",
                     "url": "http://docs.python.org/2/tutorial/",
                     "views": 104},
                    {"title": "How to Think like a Computer Scientist",
                     "url": "http://www.greenteapress.com/thinkpython/",
                     "views": 9},
                    {"title": "Learn Python in 10 Minutes",
                     "url": "http://www.korokithakis.net/tutorials/python/",
                     "views": 294}]

    django_pages = [{"title": "Official Django Tutorial",
                     "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
                     "views": 49},
                    {"title": "Django Rocks",
                     "url": "http://www.djangorocks.com/", "views": 1941},
                    {"title": "How to Tango with Django",
                     "url": "http://www.tangowithdjango.com/", "views": 194194}]

    other_pages = [{"title": "Bottle",
                    "url": "http://bottlepy.org/docs/dev/", "views": 14},
                   {"title": "Flask",
                    "url": "http://flask.pocoo.org", "views": 1941}]

    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
            "Django": {"pages": django_pages, "views": 64, "likes": 32},
            "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}}

    # could add more categories or pages if i'd like and add to dictionaries

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])

    # print out categories we have added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c


# EXEC POINT
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
