import os
from .llm_model.llm import llm
from .fetch_image.content_image import content_image
from .image_generate.generate import generate
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

        cotent_data = content.response
        script = cotent_data['script']
        social = cotent_data['social']
        context = { 'script': script, 'social':social, 'MEDIA_URL': MEDIA_URL}
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
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # print(cleaned_data)
            result = llm(cleaned_data['prompt'], cleaned_data['dispositions'], cleaned_data['platforms'])
            
            social = result['social']
            seo = result['seo']

             # image generation 
            background_color = (255, 255, 255)
            logo_size = (100, 100)
            logo_path = active_brand.logo
            image_path = content_image(seo['keyword'][0])
            website_link = active_brand.handle_or_website
            heading_font_size = 72
            body_font_size = 48
            link_font_size = 36

            # Define color

            font_style = os.path.join(BASE_DIR, "static", "BAUHS93.TTF")
            color_white = active_brand.color1
            color_black = active_brand.color2
            color_blue = active_brand.color3

            print(font_style)

            for s in social.keys():
                if s == 'facebook':
                    margin, width, height = 60, 1200, 630

                elif s == 'instagram':
                    margin, width, height = 80, 1080, 1080

                elif s == 'linkedin':
                    margin, width, height = 80, 1080, 1080

                heading = social[s]["heading"]
                body = social[s]["body"]
                image = generate(heading, body, website_link, image_path, logo_path, font_style,heading_font_size, body_font_size, link_font_size, width, height, logo_size, margin , color_white, color_black, color_blue, background_color)
                social[s]['img'] = image
            # save content
            response = ResponseModel(brand=active_brand, response=result)
            response.save()

            return redirect('contents:result', pk = response.pk)