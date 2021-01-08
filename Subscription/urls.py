from django.urls import path
from . import views


urlpatterns = [
    path('plan/', views.SubscriptionTypeView.as_view(), name='plan'),
    path('plan/<int:id>/', views.SubscriptionTypeDetails.as_view(), name='plan-details'),
]