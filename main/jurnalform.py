# from django import forms
# from .models import Journal, Souvenir

# class JournalForm(forms.ModelForm):
#     place_name = forms.ChoiceField(choices=[], required=False)
#     souvenir = forms.ModelChoiceField(queryset=Souvenir.objects.all(), required=False)

#     class Meta:
#         model = Journal
#         fields = ['title', 'content', 'image', 'place_name', 'souvenir']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Ambil unique place names dari Souvenir
#         places = Souvenir.objects.values_list('place_name', flat=True).distinct()
#         self.fields['place_name'].choices = [('', '-- Select Place --')] + [(place, place) for place in places]


from django import forms
from .models import Journal, Souvenir

class JournalForm(forms.ModelForm):
    place_name = forms.ChoiceField(choices=[], required=False)
    souvenir = forms.ModelChoiceField(queryset=Souvenir.objects.all(), required=False)
    author_username = forms.CharField(required=False, disabled=True)  # Tambahkan ini

    class Meta:
        model = Journal
        fields = ['title', 'content', 'image', 'place_name', 'souvenir', 'author_username']  # Tambahkan author_username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ambil unique place names dari Souvenir
        places = Souvenir.objects.values_list('place_name', flat=True).distinct()
        self.fields['place_name'].choices = [('', '-- Select Place --')] + [(place, place) for place in places]

        # Set username penulis jika ada
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['author_username'].initial = kwargs['instance'].author.username