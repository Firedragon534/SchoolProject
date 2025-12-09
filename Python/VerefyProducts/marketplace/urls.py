from django.urls import path
from . import views
app_name = 'marketplace'
urlpatterns = [
    path('', views.home, name='home'),
    path('listing/create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/request-test/', views.request_test, name='request_test'),
    path('verify/<int:pk>/', views.verify_listing, name='verify_listing'),
    path('chatbot/', views.chatbot_api, name='chatbot_api'),
]
