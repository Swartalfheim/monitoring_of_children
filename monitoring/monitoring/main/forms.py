# your_app_name/forms.py
from django import forms
from .models import Ditina
import re

class DitinaForm(forms.ModelForm):
    class Meta:
        model = Ditina

        fields = ['imya', 'prizvische', 'region', 'vik', 'zrist', 'pryimaie_gormony']

        labels = {
            'imya': "Ім'я дитини",
            'prizvische': "Прізвище дитини",
            'vik': "Вік (повних років)",
            'zrist': "Зріст (в сантиметрах)",
            'pryimaie_gormony': "Чи приймає дитина гормональні препарати?"
        }
        widgets = {
            'imya': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введіть ім'я"}),
            'prizvische': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'vik': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: 5'}),
            'zrist': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: 110'}),
            'pryimaie_gormony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'vik': 'Вкажіть повну кількість років.',
        }
        error_messages = {
            'imya': {
                'max_length': "Ім'я занадто довге.",
            },
        }

    def clean_imya(self):
        imya = self.cleaned_data.get('imya')
        if imya:
            if not re.match(r"^[А-Яа-яЇїІіЄєҐґA-Za-z\s'-]+$", imya):
                raise forms.ValidationError("Ім'я може містити тільки літери, пробіли, апостроф або дефіс.")
        return imya

    def clean_prizvische(self):
        prizvische = self.cleaned_data.get('prizvische')
        if prizvische:
            if not re.match(r"^[А-Яа-яЇїІіЄєҐґA-Za-z\s'-]+$", prizvische):
                raise forms.ValidationError("Прізвище може містити тільки літери, пробіли, апостроф або дефіс.")
        return prizvische

    def clean_vik(self):
        vik = self.cleaned_data.get('vik')
        if vik is not None:
            if vik > 18:
                raise forms.ValidationError("Вік не може бути більшим за 18 років для цієї форми.")
            if vik < 0:
                raise forms.ValidationError("Вік не може бути негативним.")
        return vik

    def clean_zrist(self):
        zrist = self.cleaned_data.get('zrist')
        max_reasonable_height_for_18_yo = 220
        min_reasonable_height = 20

        if zrist is not None:
            if zrist > max_reasonable_height_for_18_yo:
                raise forms.ValidationError(f"Зріст не може перевищувати {max_reasonable_height_for_18_yo} см.")
            if zrist != 0 and zrist < min_reasonable_height:
                raise forms.ValidationError(f"Зріст здається занадто малим. Мінімально допустимий зріст {min_reasonable_height} см (або 0, якщо не вказано).")
        return zrist
