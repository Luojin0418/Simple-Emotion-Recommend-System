from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
