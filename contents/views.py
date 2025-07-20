import os
from .llm_model.llm import SocialMediaGenerator
from .models import ResponseModel
from brands.models import BrandModel
from .forms import PromptForm
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# testing data
# from .test_json import test_json

# Create the views here.
BASE_DIR = settings.BASE_DIR
MEDIA_URL = settings.MEDIA_URL

# Dashboard view
class DashboardView(LoginRequiredMixin, View):
    template_name = "pages/dashboard.html"
    def get(self, request):
        return render(request, self.template_name)
    
def calander_view(request):
    return render(request, "pages/calander.html")

# Content list view
class ContentsListView(LoginRequiredMixin, View):
    template_name = "pages/contents.html" 
    # display ListView in descending order by ID - overide get_queryset
    def get(self, request):
        if BrandModel.objects.filter(user=request.user):
            brand = BrandModel.objects.get(user=request.user, is_active=True)
            responses = ResponseModel.objects.filter(brand=brand).order_by('-id')
            # print(responses)
            return render(request, self.template_name, {'responses' : responses})
        else:
            return redirect('brands:brand_list')

# full view of content
class ContentView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk is not None:
            # content = get_object_or_404(ResponseModel, pk=id)
            content = ResponseModel.objects.get(id=pk)
        else:
            # ID parameter is not provided, retrieve the latest response
            try : 
                content = ResponseModel.objects.latest('created_at')
            except ResponseModel.DoesNotExist:
                content = None

        content_data = content.response
    
        print(content_data)

        context = { 'contents': content_data['contents'], "img_url": content_data['img_url']}
        return render(request, 'content/result.html', context)

# Create content from user prompt
class PromptCreateView(LoginRequiredMixin, View):
    model = ResponseModel
    brand_model = BrandModel
    input_form = PromptForm
    template = 'content/create.html'

    def get(self, request):
        try:
            user = request.user
            active_brand = self.brand_model.objects.get(user = user, is_active=True)
            if active_brand:
                return render(request, self.template ,{'form': self.input_form()})
            else:
                return redirect("brands:brand_list")
        except BrandModel.DoesNotExist:
            return redirect("brands:brand_list")
    
    def post(self, request):
        form = self.input_form(request.POST)
        active_brand = BrandModel.objects.get(user = request.user, is_active=True)

        if active_brand:
            brand_handle_or_website = active_brand.handle_or_website
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            generate = SocialMediaGenerator()
            # print(cleaned_data)
            # result = llm(cleaned_data['prompt'], cleaned_data['dispositions'], cleaned_data['platforms'])
            topic = cleaned_data['subject']
            platforms = cleaned_data['platforms']
            context  = cleaned_data['prompt']
            tone = cleaned_data['tone']
            
            result = generate.generate_multiple_posts_with_images(topic=topic, platforms=platforms, context=context, tone=tone, brand_handle=brand_handle_or_website)
            # print("final:" , result)
            # save content
            response = ResponseModel(brand=active_brand, response=result)
            response.save()

            return redirect('contents:result', pk = response.pk)