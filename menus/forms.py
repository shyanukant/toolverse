from django import forms
from .models import ContactModel

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactModel
        fields = "__all__"
        char_class ="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light"
        widgets = {
            'name' : forms.TextInput(
                attrs={'class': char_class}
            ),
            'email': forms.TextInput(
                attrs={'class': char_class}
            ),
            'subject' : forms.TextInput(
                attrs={'class' : char_class}
            ) ,
            'message': forms.Textarea(
                attrs={'class': char_class}
            ),
            'file' : forms.FileInput(
                attrs= { 'class' : "block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400"}
            )
        }