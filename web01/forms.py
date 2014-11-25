from django.forms import *
from django import forms
from web01.models import *
class MForm(Form):
    img=forms.ImageField()
    file=forms.FilePathField(path=".")
