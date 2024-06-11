from django.contrib import admin
from django.urls import path
from .views import RecipeAPIview, RecipeDetailView, RecipeCategoryAPIview, RecipeSearchFilterView, ReviewAPIView

urlpatterns = [
    path('', RecipeAPIview.as_view(), name='recipe_main_view'),
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe-category/', RecipeCategoryAPIview.as_view(), name='recipe_category'), 

    path('search/', RecipeSearchFilterView.as_view(), name='recipe_search_filter'),

    path('<int:recipe_id>/reviews/', ReviewAPIView.as_view(), name='recipe_reviews'),
]