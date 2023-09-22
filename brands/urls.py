from django.urls import path
from  .views import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleleView, switch_brand

app_name = "brands"
urlpatterns = [
    path('', BrandListView.as_view(), name='brand_list'),
    path('create/', BrandCreateView.as_view(), name='create'),
    path('<int:pk>/update/', BrandUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', BrandDeleleView.as_view(), name='delete'),
    path('<int:pk>/switch/', switch_brand, name='switch_brand')

]