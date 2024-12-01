from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import FoodSearchForm, CalculateTDEEForm    
from .models import FoodEntry, CalculateTDEE

from tracker.models import Goal # Import Goal model from tracker

from datetime import date
import requests

# Search for food
@login_required
def search_food(request):
    if request.method == 'POST':
        form = FoodSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={settings.USDA_API_KEY}&query={query}'
            response = requests.get(url)
            data = response.json()
            return render(request, 'food_tracker/search_results.html', {
                'data': data,
            })
    else:
        form = FoodSearchForm()
    return render(request, 'food_tracker/search_food.html', {
        'form': form,
    })

# Add food entry
@login_required
def add_food_entry(request, fdc_id):
    url = f'https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={settings.USDA_API_KEY}'
    response = requests.get(url)
    data = response.json()
    food_name = data['description']
    nutrients = {nutrient['nutrient'].get('name', ''): (nutrient.get('amount', 0), nutrient['nutrient'].get('unitName', '')) for nutrient in data['foodNutrients']}

    protein, protein_unit = nutrients.get('Protein', (0, ''))
    fat, fat_unit = nutrients.get('Total lipid (fat)', (0, ''))
    carbs, carbs_unit = nutrients.get('Carbohydrate, by difference', (0, ''))

    # Ensure unit of calories is kcal
    calories = 0
    for nutrient in data.get('foodNutrients', []):
        if nutrient is None:
            continue
        if ('Energy' in nutrient['nutrient']['name']) and ('kcal' in nutrient['nutrient']['unitName']):
            calories = nutrient.get('amount', 0)
            break
    
    if request.method == 'POST':
        meal_type = request.POST.get('meal_type')
        servings = float(request.POST.get('servings', 1))

        FoodEntry.objects.create(
            user=request.user,
            food_name=food_name,
            calories=calories * servings,
            protein=protein * servings,
            fat=fat * servings,
            carbs=carbs * servings,
            meal_type=meal_type,
            servings=servings
        )
        return redirect('food_tracker:food_log')
    
    return render(request, 'food_tracker/add_food_entry.html', {
        'food_name': food_name,
        'calories': calories,
        'protein': protein,
        'fat': fat,
        'carbs': carbs,
    })

# Render the index page of the food logging app
@login_required
def food_log(request):
    today = date.today()
    meal_type = request.GET.get('meal_type', 'all')
    if meal_type == 'all':
        entries = FoodEntry.objects.filter(user=request.user, date=today).order_by('-date')
    else:
        entries = FoodEntry.objects.filter(user=request.user, date=today, meal_type=meal_type).order_by('-date')

    # All entries
    all_entries = FoodEntry.objects.filter(user=request.user, date=today).order_by('-date')

    # Calculate TDEE
    tdee_calculate = CalculateTDEE.objects.filter(user=request.user).last()
    tdee = tdee_calculate.calculate_tdee()
    recommended_calories = tdee

    # Total amount for each macro
    total_calories = sum(entry.calories for entry in all_entries)
    total_protein = sum(entry.protein for entry in all_entries)
    total_fat = sum(entry.fat for entry in all_entries)
    total_carbs = sum(entry.carbs for entry in all_entries)

    weekly_goal = 'Not set!'

    # Fetch the user's goal
    goals = Goal.objects.filter(created_by=request.user)
    if goals.exists():
        goal = goals.first()
        weekly_goal = goal.get_weekly_goal_display()
        if goal.goal_type == 'weight_loss':
            if goal.weekly_goal == 'lose_1':
                recommended_calories = tdee - 500 # Create a 500 calorie deficit
            elif goal.weekly_goal == 'lose_2':
                recommended_calories = tdee - 1000 # Create a 1000 calorie deficit
        elif goal.goal_type == 'weight_gain':
            if goal.weekly_goal == 'gain_3':
                recommended_calories = tdee + 500
            elif goal.weekly_goal == 'gain_4':
                recommended_calories = tdee + 1000
        else:
            recommended_calories = tdee # Maintenance
    else:
        recommended_calories = tdee # Default to maintenance if no goals are found
    
    calories_left = recommended_calories - total_calories
    # Calculate calories over
    calories_over = 0
    if calories_left < 0:
        calories_over = -calories_left

    # Calculate the percentage of calories consumed
    if recommended_calories > 0:
        calories_percentage = (total_calories / recommended_calories) * 100
    else:
        calories_percentage = 0

    # Meals
    meals = ['breakfast', 'lunch', 'dinner', 'snacks']

    return render(request, 'food_tracker/food_log.html', {
        'entries': entries,
        'tdee': tdee,
        'calories_left': round(calories_left),
        'recommended_calories': recommended_calories,
        'weekly_goal': weekly_goal,
        'calories_over': round(calories_over),
        'total_calories': round(total_calories),
        'total_protein': round(total_protein),
        'total_fat': round(total_fat),
        'total_carbs': round(total_carbs),
        'meal_type': meal_type,
        'calories_percentage': calories_percentage,
        'meals': meals,
    })

@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(FoodEntry, pk=pk, user=request.user)

    return render(request, 'food_tracker/entry_detail.html', {
        'food_name': entry.food_name,
        'calories': entry.calories,
        'protein': entry.protein,
        'fat': entry.fat,
        'carbs': entry.carbs,
        'servings': entry.servings,
    })

@login_required
def calculate_tdee(request):
    if request.method == 'POST':
        form = CalculateTDEEForm(request.POST)
        if form.is_valid():
            tdee = form.save(commit=False)
            tdee.user = request.user
            tdee.save()
            return redirect('food_tracker:food_log')
    else:
        form = CalculateTDEEForm()
    return render(request, 'food_tracker/calculate_tdee.html', {
        'form': form,
    })

@login_required
def delete_food_entry(request, pk):
    food_entry = get_object_or_404(FoodEntry, pk=pk, user=request.user)
    food_entry.delete()
    return redirect('food_tracker:food_log')

