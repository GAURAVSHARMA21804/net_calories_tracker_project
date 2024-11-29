from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'tracker/home.html')
@login_required
def user_dashboard(request):
    return render(request, 'tracker/users_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'tracker/admin_panel_dashboard.html')

from django.http import JsonResponse
from .models import FoodData,DailyFoodLog,MealType,ActivityData,DailyActivityLog
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_date
from datetime import datetime

def search_food(request):
    query = request.GET.get('query', '')
    if query:
        foods = FoodData.objects.filter(food_name__icontains=query).values('food_id', 'food_name', 'food_group')
        food_list = list(foods)
        return JsonResponse({'foods': food_list})
    return JsonResponse({'foods': []})



def save_food_log(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract values from the JSON data
            date = data.get('date')
            food_id = data.get('food_item')
            meal_type = data.get('meal_type')
            serving_count = data.get('serving_count')

            # Validate the required fields
            if not date or not food_id or not meal_type or not serving_count:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Ensure serving_count is a float
            try:
                serving_count = float(serving_count)
            except ValueError:
                return JsonResponse({"error": "Invalid serving count"}, status=400)

            # Fetch the food item from the database using food_id
            try:
                food_item = FoodData.objects.get(food_id=food_id)
            except FoodData.DoesNotExist:
                return JsonResponse({"error": "Food item not found"}, status=400)

            # Check if the meal type exists
            try:
                meal_type_obj = MealType.objects.get(name=meal_type)
            except MealType.DoesNotExist:
                return JsonResponse({"error": "Meal type not found"}, status=400)

            # Parse the date
            try:
                food_date = datetime.strptime(date, '%Y-%m-%d').date()  # Adjust the format based on your input
            except ValueError:
                return JsonResponse({"error": "Invalid date format"}, status=400)

            # Create a new DailyFoodLog entry
            daily_food_log = DailyFoodLog(
                user=request.user,  # Assuming user is logged in
                date=food_date,
                food_item=food_item,
                meal_type=meal_type_obj,
                serving_count=serving_count,
            )

            # Ensure food_item.calories is a float
            try:
                food_item_calories = float(food_item.calories)  # Make sure it's a float
            except ValueError:
                return JsonResponse({"error": "Invalid calories value"}, status=400)

            daily_food_log.total_calories = serving_count * food_item_calories

            daily_food_log.save()

            # Return a success response
            return JsonResponse({"message": "Food log added successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def search_activity(request):
    query = request.GET.get('query', '')
    if query:
        activities = ActivityData.objects.filter(activity_name__icontains=query).values('activity_id', 'activity_name', 'specific_motion', 'mets')
        activity_list = list(activities)
        return JsonResponse({'activities': activity_list})
    return JsonResponse({'activities': []})

def save_activity_log(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract values from the JSON data
            date = data.get('date')
            activity_id = data.get('activity_id')
            duration_minutes = data.get('duration_minutes')
            description = data.get('description', '')

            # Validate the required fields
            if not date or not activity_id or not duration_minutes:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Ensure duration_minutes is an integer
            try:
                duration_minutes = int(duration_minutes)
                if duration_minutes <= 0:
                    return JsonResponse({"error": "Duration must be greater than zero"}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid duration value"}, status=400)

            # Fetch the activity item from the database using activity_id
            try:
                activity_item = ActivityData.objects.get(activity_id=activity_id)
            except ActivityData.DoesNotExist:
                return JsonResponse({"error": "Activity not found"}, status=400)

            # Parse the date
            try:
                activity_date = parse_date(date)  # Parse the date from the string
                if not activity_date:
                    raise ValueError("Invalid date format")
            except ValueError:
                return JsonResponse({"error": "Invalid date format"}, status=400)

            # Create a new DailyActivityLog entry
            daily_activity_log = DailyActivityLog(
                user=request.user,  # Assuming user is logged in
                date=activity_date,
                activity=activity_item,
                duration_minutes=duration_minutes,
                description=description,
            )

            # The save method of the DailyActivityLog model will automatically calculate calories_burned
            daily_activity_log.save()

            # Return a success response
            return JsonResponse({"message": "Activity log added successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)
