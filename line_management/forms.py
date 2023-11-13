from django import forms


class DowntimeCreateForm(forms.Form):
    employee = forms.CharField()
    line = forms.CharField()


class DowntimeUpdateForm(forms.Form):
    employee = forms.CharField()
    reason = forms.CharField()
    comments = forms.CharField()
