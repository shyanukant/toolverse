from django.shortcuts import render, redirect
from .forms import ContactForm
import json
from django.contrib import messages

# Create your views here.

def home_view(request):
    return render(request, "menus/landing.html")


def price_view(request):
    return render(request, "menus/price.html")

def about_view(request):
    return render(request, "menus/about.html")

def contact_view(request):
    faq = {
    "faq1" : { "ques" : " How many posts can I generate with a free Toolverse account?",
        "ans" : "Currently, free Toolverse accounts allow you to generate up to 30 posts per account." },
    "faq2" : {
        "ques" : " Can I manage multiple brands on Toolverse?",
        "ans" : "Yes, you can manage up to three brand profiles with a free account. Stay tuned for our Pro version, which will offer unlimited brand profiles."
    },
    "faq3" : {
        "ques" : "Is there a post scheduling feature on Toolverse?",
        "ans" : "Not yet, but it's coming soon! We're working on a post scheduler that will allow you to schedule your posts across various platforms."
    },
    "faq4" : {
        "ques" : "Can I edit my posts after they've been generated?",
        "ans" : "Currently, post editing is not available, but we're working on a content editor that will allow you to make modifications to your posts. "
    },
    "faq5" : {
        "ques" : "Are video content creation features available on Toolverse?",
        "ans" : "Video content creation is not available at the moment, but it's on our roadmap. We're excited to introduce a feature that will let you create video content from your prompts. "
    },
    "faq6" : {
        "ques" : "How long is my data stored in the Toolverse database?",
        "ans" : "Your data is automatically deleted after 7 days to ensure privacy and data management. "
    },
    "faq7" : {
        "ques" : "Is there a paid version of Toolverse?",
        "ans" : "Yes, we're working on a Pro version that will offer additional features and capabilities. Stay tuned for more details."
    }
}
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for reaching out! Your message has been received. We'll get back to you shortly.")
            return redirect('menus:contact')
        else:
            messages.warning(request, "Something went wrong")
    form = ContactForm()
    return render(request, 'menus/contact.html', { 'form': form, 'faq': faq})

def custom_404(request, exception):
    return render(request, "menus/404.html", status=404)