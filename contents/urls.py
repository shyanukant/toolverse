from django.urls import path
from  .views import DashboardView, PromptCreateView, ContentView, ContentsListView, calander_view

app_name = "contents"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('calander/', calander_view, name='calander'),
    path('create/', PromptCreateView.as_view(), name='create'),
    path('result/<int:pk>', ContentView.as_view(), name='result'),
    path('contentslist/', ContentsListView.as_view(), name="content_list"),
]