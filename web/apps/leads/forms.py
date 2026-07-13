import re

from django import forms

from apps.leads.models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "name",
            "phone",
            "email",
            "project",
            "unit_type",
            "budget",
            "message",
            "language",
            "page_url",
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_content",
            "utm_term",
            "fbp",
            "fbc",
        ]

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        normalized = re.sub(r"[\s().-]", "", phone)
        if not re.match(r"^\+?\d{8,15}$", normalized):
            raise forms.ValidationError("Please enter a valid phone number.")
        return normalized
