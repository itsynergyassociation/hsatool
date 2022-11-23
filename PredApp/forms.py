from django import forms


class PredictForm(forms.Form):
    Global_radiation = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Surface_temperature = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Air_temperature = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Relative_Humidity = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    Wind_speed = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class TMRTForm(forms.Form):
    vlow = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'vlow', 'placeholder':'Value less than ...'}))
    low = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'low', 'placeholder':'Value less than ...'}))
    medium = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'medium', 'placeholder':'Value less than ...'}))
    high = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'high', 'placeholder':'Value less than ...'}))
    vhigh = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'vhigh', 'placeholder':'Value greater than ...'}))


class PMVForm(forms.Form):
    hot = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'hot', 'placeholder':'Value greater than ...'}))
    warm = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'warm', 'placeholder':'Value greater than ...'}))
    slwarm = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'slwarm', 'placeholder':'Value greater than ...'}))
    neutral = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'neutral', 'placeholder':'Value less than ...'}))
    slcool = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'slcool', 'placeholder':'Value less than ...'}))
    cool = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cool', 'placeholder':'Value less than ...'}))
    cold = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cold', 'placeholder':'Value less than ...'}))


class PETForm(forms.Form):
    vcold = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'vcold', 'placeholder':'Value less than ...'}))
    petcold = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'petcold', 'placeholder':'Value less than ...'}))
    petcool = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'petcool', 'placeholder':'Value less than ...'}))
    petslcool = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'petslcool', 'placeholder':'Value less than ...'}))
    comfort = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'comfort', 'placeholder':'Value less than ...'}))
    petslwarm = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'petslwarm', 'placeholder':'Value less than ...'}))
    petwarm = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'petwarm', 'placeholder':'Value less than ...'}))
    pethot = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pethot', 'placeholder':'Value less than ...'}))
    vhot = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'vhot', 'placeholder':'Value greater than ...'}))