from django.forms import ModelMultipleChoiceField
from django_filters.rest_framework import (
    FilterSet, CharFilter,
    ModelChoiceFilter, NumberFilter,
)

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientFilters(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilters(FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
    )
    is_favorited = NumberFilter(
        method='is_favorited_filter',
        field_name='is_favorited'
    )
    is_in_shopping_cart = NumberFilter(
        method='is_in_shopping_list_filter',
        field_name='is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def is_favorited_filter(self, queryset, name, value):
        if value == 1 and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def is_in_shopping_list_filter(self, queryset, name, value):
        if value == 1 and self.request.user.is_authenticated:
            return Recipe.objects.filter(
                shopping_cart__user=self.request.user
            )
        return queryset
