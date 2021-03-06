from django.http import Http404
from django.shortcuts import get_object_or_404
from food.models import Food, FoodCategory
from recipe.models import RecipeCategory, Recipe
from django.views.generic import DetailView, ListView

class FoodDetailView(DetailView):
	queryset = Food.objects.all()

	def get_object(self):
		object = super(FoodDetailView, self).get_object();

		object.view_num = object.view_num + 1
		object.save()

		return object

	def get_context_data(self, **kwargs):
		context = super(FoodDetailView, self).get_context_data(**kwargs)
		context['category_list'] = FoodCategory.objects.filter(id__gt=1)
		context['recipe_list'] = context['object'].recipe_set.all().only('name', 'cover_image', 'did_num', 'like_num', 'date', 'view_num')
		return context


class FoodCategoryDetailView(DetailView):
	model = FoodCategory
	template_name = 'food/food_list.html'
	context_object_name = "category"
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(FoodCategoryDetailView, self).get_context_data(**kwargs)
		context['food_list'] = Food.objects.filter(category=context['category'])
		context['category_list'] = FoodCategory.objects.filter(id__gt=1)
		return context


def categories(request):
	fc = FoodCategory.objects.all()
	rc = RecipeCategory.objects.all().defer('brief')
	return render(request, 'food/categories.html', {'foodcategory': fc, 'recipecategory':rc})
