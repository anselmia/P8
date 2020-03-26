from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'search_input', 'name':"text", 'id' : "text", 'placeholder':"Trouver le meilleur substitut" }))

    def clean_search(self):
        cleaned_data = super(SearchForm, self).clean()
        text = cleaned_data.get('search')
        text = self.remove_spec_char(text)

        if text == "":
            raise forms.ValidationError(
                    "le produit recherché est invalide"
                )

        return text  # N'oublions pas de renvoyer les données si tout est OK
    
    def remove_spec_char(self, text):
        for ch in [
            "\\",
            "`",
            "*",
            "_",
            "{",
            "}",
            "[",
            "]",
            "(",
            ")",
            ">",
            "#",
            "+",
            "-",
            ".",
            "!",
            "$",
            "^",
            "?",
            "'",
            "&",
            '"',
            "=",
            ",",
            ":",
            ";",
            "/",
        ]:
            if ch in text:
                text = text.replace(ch, "")

        return text