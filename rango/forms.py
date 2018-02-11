from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    #inline clas to provide additional information on the form
    class Meta:
        #creating association between ModelForm and a Model
        model = Category
        fields= ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        #If url is not empty and doesnt start with http://
        #prepend it
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

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