from django import forms

from core.tools import get_week_list


class IndexPageForm(forms.Form):
    choice_list = []
    for idx, i in enumerate(get_week_list(True)):
        choice_list.append((idx, i))
    week = forms.ChoiceField(choices=choice_list)
