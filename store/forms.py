from django import forms
from jalali_suite.forms import JalaliDateField

class OrderDateRangeForm(forms.Form):
    start_date= JalaliDateField(required=False)
    end_date = JalaliDateField(required=False)