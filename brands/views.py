from .models import BrandModel
from .forms import BrandForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
class BrandListView(LoginRequiredMixin, View):
    template_name = "pages/brands.html"
    def get(self, request):
        brands = BrandModel.objects.filter(user = request.user)
        return render(request, self.template_name, {'brands':brands})

class BrandCreateView(LoginRequiredMixin, View):
    template_name = "brands/brand.html"
    success_url = reverse_lazy('contents:create')

    def get(self, request):
        form = BrandForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        user = request.user
        form = BrandForm(request.POST, request.FILES)
        user_brand_profiles = BrandModel.objects.filter(user=user)
        # set limit of brand - 3
        if user_brand_profiles.count() < 3:
            if form.is_valid():
                # deactivate old brand_prfile when creating new 
                if user_brand_profiles.count() > 0:
                    for profile in user_brand_profiles:
                        profile.is_active = False
                        profile.save()
                # Create the new brand profile and set it as active
                brand_profile = form.save(commit=False)
                brand_profile.user = user
                brand_profile.is_active = True
                brand_profile.save()
                return redirect(self.success_url)
            else:
                return render(request, self.template_name, {'form':form})
        else:
            messages.warning(request, "You have reach the maximum limit of brand.")
            return redirect("brands:brand_list")


class BrandUpdateView(LoginRequiredMixin, View):
    model = BrandModel
    form = BrandForm
    template_name = "brands/brand.html"
    success_url = reverse_lazy('contents:create')

    def get(self, request, pk):
        brand = get_object_or_404(self.model, id=pk, user=request.user)
        brand_info = self.form(instance=brand)
        return render(request, self.template_name, {'form' : brand_info})
    
    def post(self, request, pk):
        brand = get_object_or_404(self.model, id=pk, user=request.user)
        brand_info = self.form(request.POST, instance=brand)
        if not brand_info.is_valid():
            return render(request, self.template_name, {{'form' : brand_info}})
        brand_info.save()   
        return redirect(self.success_url) 

class BrandDeleleView(LoginRequiredMixin, View):
    model = BrandModel
    
    def post(self, request, pk):
        brand = get_object_or_404(self.model, id=pk, user=request.user)
        brand.delete()   
        messages.error(request, f"{brand.brand_name} Brand profile deleted successfully!")
        return JsonResponse({'success': True})  
    
def switch_brand(request, pk):
    if request.method == 'POST':
        user = request.user
        try :
            selected_brand = BrandModel.objects.get(id=pk, user=user)
        except BrandModel.DoesNotExist:
            return JsonResponse({ 'success':False, 'message': "Invalid brand selections. "})
        
        # deactivate other brand
        user_brand_profiles = BrandModel.objects.filter(user=user)
        for profile in user_brand_profiles:
            if profile == selected_brand:
                profile.is_active = True
            else:
                profile.is_active = False
            profile.save()
        messages.success(request, f"{selected_brand.brand_name} Brand activated successfully|")
        return JsonResponse({'success': True})

    return redirect('brands:brand_list')
