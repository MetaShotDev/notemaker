from django import forms

PROCESSING_CHOICES = [
    ('video', 'Video'), 
    ('audio', 'Audio'),
    ('both', 'Both')
]

NOTETYPE_CHOICES = [
    ('onecolumn', 'One Column'),
    ('twocolumn', 'Two Column'),
]

class NoteForm(forms.Form):
    youtubeLink = forms.CharField(label='Youtube Link', max_length=1024)
    # drop down with video or audio or both
    # drop down with note type
    processing = forms.ChoiceField(
        label='Processing', 
        choices=PROCESSING_CHOICES, 
        widget=forms.RadioSelect
    )
    noteType = forms.CharField(
        label='Note Type', 
        max_length=1024,
        widget=forms.Select(choices=NOTETYPE_CHOICES)
    )

    class Meta:
        fields = ['youtubeLink',]