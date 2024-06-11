from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    owner = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    preparation_steps = models.TextField()
    cooking_time = models.PositiveIntegerField()
    serving_size = models.PositiveIntegerField()
    categories = models.ManyToManyField(RecipeCategory, related_name='recipes')
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title
    
    def update_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        else:
            self.average_rating = 0.0
        self.save()

class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.update_average_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.recipe.update_average_rating()
    