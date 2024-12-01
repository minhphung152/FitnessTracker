from django.db import models
from django.contrib.auth.models import User

class FoodEntry(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    date = models.DateField(auto_now_add=True)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES, default='breakfast')
    servings = models.FloatField(default=1)

    class Meta: 
        verbose_name_plural = 'Food Entries'

    def __str__(self):
        return f'{self.food_name} - {self.calories} kcal'
    
class CalculateTDEE(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        (1.2, 'Sedentary (little or no exercise)'),
        (1.375, 'Lightly active (light exercise/sports 1-3 days/week)'),
        (1.55, 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        (1.725, 'Very active (hard exercise/sports 6-7 days a week)'),
        (1.9, 'Super active (very hard exercise/sports & physical job)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.FloatField() # in lbs
    height = models.FloatField() # in in
    activity_level = models.FloatField(choices=ACTIVITY_LEVEL_CHOICES)

    def calculate_bmr(self):
        if self.gender == 'M':
            return 10 * (self.weight * 0.453592) + 6.25 * (self.height * 2.54) - 5 * self.age + 5
        else:
            return 10 * (self.weight * 0.453592) + 6.25 * (self.height * 2.54) - 5 * self.age - 161
    
    def calculate_tdee(self):
        bmr = self.calculate_bmr()
        return round(bmr * self.activity_level)
    
    def __str__(self):
        return f'{self.user.username} - TDEE: {self.calculate_tdee()}'

