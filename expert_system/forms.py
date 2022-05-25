from .models import Result
from django.forms import ModelForm


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields =all()
