# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.conf import settings

import uuid
from django.db import models
from django.db.models.fields import DateField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.core import validators

from djmoney.models.fields import MoneyField

from django.urls import reverse

import random   
import string  
import secrets 

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from mimetypes import guess_type









# GENERATE RANDOM STRING WITH LENGTH 
def random_string(num):   
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
    return str(res)







# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('is_superuser should be True'))
        extra_fields['is_staff'] = True
        return self.save_user(email, password, **extra_fields) 
    





ROLE = (
    ("User", _("User")),
    ("Agent", _("Agent")),
)

class User(AbstractBaseUser, PermissionsMixin):
    id        = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name      = models.CharField(_("Name"), max_length=100,)
    email     = models.EmailField(_("Email"), max_length=200, unique=True, validators = [validators.EmailValidator()])
    is_staff  = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    i_agree   = models.BooleanField(_("Terms and conditions"), blank=True, null=True, default=False)
    role      = models.CharField(_("Role"), max_length=100, choices=ROLE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.name








POSITION = (
    ("1_month", _("1 month($10)")),
    ("3_months", _("3 months($25)")),
    ("6_months", _("6 months($50)")),
    ("12_months", _("12 months($100)")),
)
# MONTHLY USE MODEL
class MonthlyPayment(models.Model):
    reference  = models.CharField(_("Reference"), max_length=255, null=False, blank=False, unique=True)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="monthly_use_user")
    option     = models.CharField(_("Options"), max_length=100, choices=POSITION, null=False, blank=False)
    amount     = models.DecimalField(_("Amount"), decimal_places=2, max_digits=5, null=False, blank=False)
    start_date = models.DateField(_("Start Date"), blank=False, null=False)
    end_date   = models.DateField(_("End Date"), blank=False, null=False)
    paid       = models.BooleanField(_("Paid"), default=False)
    active     = models.BooleanField(_("Active"), default=True)
    timestamp  = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)


    def __str__(self):
        return self.user.name


    class Meta:
        ordering = ("-timestamp",)


