from django import forms

from news_app.models import News


class PostCreationForm(forms.ModelForm):
    STATUSES = [
        ('DRAFT', 'Черновик'),
        ('APPROVED', 'Готова к публикации'),
    ]
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название'
    }))
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Текст',
        'rows': '10',
        'style': "height:100%;"
    }))
    topic = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Топик'
    }))
    status = forms.ChoiceField(widget=forms.Select(attrs={
        'placeholder': 'Черновик'
    }), choices=STATUSES)

    photo = forms.ImageField(widget=forms.widgets.FileInput, required=False)

    class Meta:
        model = News
        fields = (
            'title',
            'text',
            'topic',
            'status',
            'photo',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'photo':
                field.widget.attrs['type'] = 'file'
                field.widget.attrs['id'] = 'Photo'
            if field_name == 'status':
                field.widget.attrs['id'] = 'floatingSelect'
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['id'] = 'floatingInput'

