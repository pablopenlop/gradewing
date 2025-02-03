from django import forms
from datetime import datetime

class MonthField(forms.Field):
    def to_python(self, value):
        if not value:
            return None
        try:
            return datetime.strptime(value, '%Y-%m')
        except ValueError:
            raise forms.ValidationError("Invalid month format. Use YYYY-MM.")

    def validate(self, value):
        super().validate(value)
        if value and not isinstance(value, datetime):
            raise forms.ValidationError("Invalid date type.")
