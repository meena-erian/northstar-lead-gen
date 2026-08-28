from django import forms
from .models import Lead
class LeadForm(forms.ModelForm):
    consent = forms.BooleanField(label="I agree to be contacted about Northstar.")
    class Meta:
        model = Lead
        fields = ["name","email","company","message","consent"]
        labels = {"email":"Work email", "message":"What would you like to improve?"}
        widgets = {"name":forms.TextInput(attrs={"placeholder":"Your name"}),"email":forms.EmailInput(attrs={"placeholder":"you@company.com"}),"company":forms.TextInput(attrs={"placeholder":"Company (optional)"}),"message":forms.Textarea(attrs={"rows":3,"placeholder":"Tell us about your growth goal (optional)"})}
    def clean_email(self): return self.cleaned_data["email"].strip().lower()
