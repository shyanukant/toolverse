from django.urls import path
from .views import home_view, price_view, about_view ,contact_view

app_name = 'menus'
urlpatterns = [
    path("", home_view, name='home'),
    path("price/", price_view, name='price'),
    path("about-us/", about_view, name='about'),
    path("contact-us/", contact_view, name='contact'),
]