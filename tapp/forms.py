from django import forms


from .models import Product , Case , Customer


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['customer', 'product', 'title', 'description1','description2' ,'start_time', 'end_time','status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),  # customer alanı için stil
            'product': forms.Select(attrs={'class': 'form-control'}), 
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description1': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description1'}),
            'description2': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description2'}),
            'start_time': forms.TimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.TimeInput(attrs={'type': 'datetime-local'}),
        }

class CaseFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))


