from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from core.models import Recipe


def redirect_to_recipe(request, hash_url):
    recipe = get_object_or_404(Recipe, hash_url=hash_url)
    full_url = f'/recipes/{recipe.id}'
    return HttpResponseRedirect(full_url)
