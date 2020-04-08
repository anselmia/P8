""" Home App Forms """

from django import forms
import re


class SearchForm(forms.Form):
    """ Form user to search product """

    search = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "search_input",
                "name": "text",
                "placeholder": "Rechercher...",
            }
        ),
    )

    def clean_search(self):
        """Search text validation"""

        cleaned_data = super(SearchForm, self).clean()
        text = cleaned_data.get("search")
        text = re.sub(r"\W+", "", text)

        if text == "":
            raise forms.ValidationError("le produit recherché est invalide")

        return text
