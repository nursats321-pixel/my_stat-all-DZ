from django.urls import path

from . import views


urlpatterns = [
    path("products/", views.products),
    path("products/<str:product_id>/", views.product_detail),
]