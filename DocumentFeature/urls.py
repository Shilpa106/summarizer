from django.urls import path
from . import views

urlpatterns = [
        path('', views.FeaturesList.as_view(), name='feature-list'),
        path('<int:id>/<int:doc_id>/', views.FeatureView.as_view(), name='feature-view'),
]
