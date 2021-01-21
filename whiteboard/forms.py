from django import forms
from .models import people


class peopleForm(forms.ModelForm):

    class Meta:
        model=people
        fields=('user','employeeID','extension_num','circuleNum','frequent')
        labels={'employeeID':'NO. ','extension_num':'ext. ','circuleNum':'Count'}
        widgets = {'circuleNum': forms.TextInput(attrs={'size': '5'}),}

class adminForm(forms.ModelForm):

    class Meta:
        model=people
        fields=('user','employeeID','extension_num','circuleNum','frequent','cutline')
        labels={'employeeID':'NO. ','extension_num':'ext. ','cutline':'插測 ','circuleNum':'Count'}
        widgets = {'circuleNum': forms.TextInput(attrs={'size': '5'}),}