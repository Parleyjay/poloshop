from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime, date
from backend.models import Product

from . import forms