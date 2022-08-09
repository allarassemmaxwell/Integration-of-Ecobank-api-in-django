from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import *

from django.core.files.images import get_image_dimensions
User = get_user_model()

from django.forms.widgets import CheckboxInput
from datetime import date







# MONTHLY PAYMENT FORM
class MonthlyPaymentForm(forms.ModelForm):
    class Meta:
        model  = MonthlyPayment
        fields = [
            "option",
        ]
        widgets = {
            'option':    forms.Select(attrs={'class': 'form-control select2', 'data-toggle':'select2'}),
        }

