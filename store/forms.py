from django import forms
from jalali_suite.forms import JalaliDateField
from jalali_suite.widgets import AdminJalaliDateWidget

class OrderDateRangeForm(forms.Form):
    start_date = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget()
    )
    end_date = JalaliDateField(
        required=False,
        widget=AdminJalaliDateWidget()
    )