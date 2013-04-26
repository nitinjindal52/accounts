from models import *
from django.forms import ModelForm


class AccountForm(ModelForm):
    class Meta:
        model = Account
        
class Sub_AccountForm(ModelForm):
    class Meta:
        model = Sub_Accountt