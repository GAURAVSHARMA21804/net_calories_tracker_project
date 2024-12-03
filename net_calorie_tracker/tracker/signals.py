from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.apps import apps
from datetime import date
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender='tracker.DailyFoodLog')
@receiver(post_save, sender='tracker.DailyActivityLog')
@receiver(post_delete, sender='tracker.DailyFoodLog')
@receiver(post_delete, sender='tracker.DailyActivityLog')
def update_daily_summary(sender, instance, **kwargs):
    """
    Updates the daily summary table whenever a food or activity log is added or deleted.
    Ensures BMR is calculated only once per day and weight is updated only at the end of the day.
    """
    # Lazy load models
    DailySummary = apps.get_model('tracker', 'DailySummary')

    user = instance.user
    log_date = instance.date

    # Retrieve or create DailySummary
    daily_summary, created = DailySummary.objects.get_or_create(user=user, date=log_date)

    # Aggregate daily data
    total_calories_in = apps.get_model('tracker', 'DailyFoodLog').objects.filter(
        user=user, date=log_date
    ).aggregate(total=Sum('total_calories'))['total'] or 0

    total_calories_out = apps.get_model('tracker', 'DailyActivityLog').objects.filter(
        user=user, date=log_date
    ).aggregate(total=Sum('calories_burned'))['total'] or 0

    # Calculate BMR only once per day
    if created or not daily_summary.bmr:
        daily_summary.bmr = user.calculate_bmr()  # Use the current weight
        daily_summary.save(update_fields=['bmr'])

    # Calculate net calories
    net_calories = total_calories_in - (total_calories_out + daily_summary.bmr)
    daily_summary.calories_in = total_calories_in
    daily_summary.calories_out = total_calories_out
    daily_summary.net_calories = net_calories
    daily_summary.save(update_fields=['calories_in', 'calories_out', 'net_calories'])

    # Update weight at the end of the day
    if log_date == date.today():
        schedule_weight_update(user, net_calories, log_date)


def schedule_weight_update(user, net_calories, log_date):
    """
    Updates the user's weight at the end of the day based on net calories
    and logs the change in WeightHistory.
    """
    from django.utils.timezone import now
    from threading import Timer

    # Schedule the weight update to run at 23:59
    current_time = now()
    end_of_day = current_time.replace(hour=23, minute=59, second=0, microsecond=0)
    delay = (end_of_day - current_time).total_seconds()

    Timer(delay, update_user_weight, args=[user, net_calories, log_date]).start()


def update_user_weight(user, net_calories, log_date):
    """
    Executes the weight update based on net calories.
    """
    WeightHistory = apps.get_model('tracker', 'WeightHistory')

    # Calculate weight change
    weight_change = round(net_calories / 7700, 2)  # 7700 kcal = 1 kg
    new_weight = user.weight + weight_change

    # Log weight change
    WeightHistory.objects.create(user=user, weight=new_weight, date=log_date)

    # Update user's weight
    user.weight = new_weight
    user.save(update_fields=['weight'])

    # Recalculate and cache BMR for the new day
    updated_bmr = user.calculate_bmr()
    user.last_calculated_bmr = updated_bmr
    user.save(update_fields=['last_calculated_bmr'])

