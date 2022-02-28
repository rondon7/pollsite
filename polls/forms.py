from django import forms
from .models import Poll_question, Poll_option

class PollAddForm(forms.ModelForm):
    # choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1,
    #                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    # choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1,
    #                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll_question
        fields = ['question_body', 'is_single']
        widgets = {
            'question_body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll_question
        fields = ['question_body', ]
        widgets = {
            'question_body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Poll_option
        fields = ['option_body', ]
        widgets = {
            'option_body': forms.TextInput(attrs={'class': 'form-control', })
        }
