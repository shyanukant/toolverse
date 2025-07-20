from django import forms
from .models import BrandModel
from django.core.exceptions import ValidationError

char_class = 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
# choice_class = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'


# Brand form

class BrandForm(forms.ModelForm):
    class Meta:
        model = BrandModel
        fields = ['brand_name', 'handle_or_website', 'logo']

        widgets = {
            'brand_name' : forms.TextInput(attrs={'class': char_class}) ,
            'handle_or_website': forms.TextInput(attrs={'class': char_class})
            ,
            'logo': forms.FileInput(
                attrs={'class': "block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}),

     
    }
  
        
    def clean(self) :
        cleaned_data = super().clean()
        