from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RecipeSerializer, RecipeCategorySerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Recipe, RecipeCategory
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class RecipeAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        related_recipe = Recipe.objects.filter(owner=self.request.user)
        related_recipe_serializer = RecipeSerializer(related_recipe, many=True)
        print(related_recipe_serializer.data)
        return Response(related_recipe_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        recipe_serializer = RecipeSerializer(data = request.data)
        if recipe_serializer.is_valid():
            recipe_serializer.save(owner=request.user)
            return Response({"Message": "Recipe Saved Succesfully"}, status=status.HTTP_201_CREATED)
        return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Recipe.objects.get(pk=pk, owner=user)
        except:
            raise Http404

    def get(self, request, pk):
        recipe = self.get_object(pk, request.user)
        serializer = RecipeSerializer(recipe)
        return Response({"Message": "Recipe Found", "data":serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        recipe = self.get_object(pk, request.user)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Recipe Updated", "data":serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        recipe = self.get_object(pk, request.user)
        serializer = RecipeSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Recipe Updated", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = self.get_object(pk, request.user)
        recipe.delete()
        return Response({"Message": "Recipe Deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class RecipeCategoryAPIview(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]
        
    def get(self, request):
        recipe_category = RecipeCategory.objects.all()
        recipe_category_serializer = RecipeCategorySerializer(recipe_category, many=True)
        print(recipe_category_serializer.data)
        return Response(recipe_category_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        recipe_category_serializer = RecipeCategorySerializer(data = request.data)
        if recipe_category_serializer.is_valid():
            recipe_category_serializer.save()
            return Response({"Message": "Recipe Category Saved Succesfully"}, status=status.HTTP_201_CREATED)
        return Response(recipe_category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RecipeSearchFilterView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = Recipe.objects.all()
        category = request.query_params.get('category')
        ingredients = request.query_params.get('ingredients')
        max_cooking_time = request.query_params.get('max_cooking_time')

        if category:
            try:
                get_category_obj = RecipeCategory.objects.get(name = category)
                queryset = Recipe.objects.filter(categories=get_category_obj)
            except:
                raise Http404
        if ingredients:
            queryset = queryset.filter(ingredients__icontains=ingredients)
        if max_cooking_time:
            queryset = queryset.filter(cooking_time__lte=max_cooking_time)


        serializer = RecipeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            raise Http404
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)