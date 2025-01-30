from django import forms
from .models import CalculateTDEE

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class FoodSearchForm(forms.Form):
    query = forms.CharField(
        label='Search for food', 
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'py-4 px-6 rounded-xl border'})
    )

class HeightField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(min_value=0, label='Feet'),
            forms.IntegerField(min_value=0, label='Inches'),
        )
        super().__init__(fields, *args, **kwargs)
    
    def compress(self, data_list):
        if data_list:
            feet = data_list[0]
            inches = data_list[1]
            total_inches = (feet * 12) + inches
            return total_inches
        return None
    
class HeightWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={
                'placeholder': 'Feet',
                'class': 'border rounded-xl px-4 py-2 w-24',
                'min': 0,
                'max': 8,
            }),
            forms.NumberInput(attrs={
                'placeholder': 'Inches',
                'class': 'border rounded-xl px-4 py-2 w-24', 
                'min': 0,
                'max': 11,
            }),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value: 
            feet = value // 12
            inches = value % 12
            return [feet, inches]
        return [0, 0]

class CalculateTDEEForm(forms.ModelForm):
    height = HeightField(widget=HeightWidget())
    
    class Meta:
        model = CalculateTDEE
        fields = ('age', 'gender', 'weight', 'height', 'activity_level', )
        widgets = {
            'age': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'gender': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'weight': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'activity_level': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            
        }