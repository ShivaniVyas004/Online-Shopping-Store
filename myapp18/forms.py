from django import forms
from myapp18.models import Order,Client

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Client
        fields = ['username','first_name','last_name','email', 'password', 'company', 'shipping_address', 'province', 'city']
        widgets = {
            'province': forms.RadioSelect
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        widgets = {
            'client': forms.RadioSelect
        }
        labels = {
            "client": "Client Name",
            "num_units": "Quantity"
        }

class InterestForm(forms.Form):
    INTEREST = [
        (0,'NO'),
        (1, 'YES')]
    interested = forms.ChoiceField(choices=INTEREST, widget=forms.RadioSelect)
    quantity = forms.IntegerField(required=True, min_value=1)
    comments = forms.CharField(label="Additional Comments", widget=forms.Textarea)