from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget.forms.HiddenInput(), required=False)

    #inline clas to provide additional information on the form
    class Meta:
        #creating association between ModelForm and a Model
        model = Category
        fields= ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_lenght=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        #assocation between ModelForm and model
        model = Page

    #What fields do we want to include in our form?
    #Dont need every field in the model present
    #some fields allow nulls so we might not want to include them
    #we hide the foreign key here
    exclude = ('category',)
    #or we can just do include and not have the category field e.g.
    #e.g. fields=('title','url','views)