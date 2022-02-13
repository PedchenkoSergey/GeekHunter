from django.forms.widgets import Textarea


class BigTextarea(Textarea):
    def __init__(self):
        default_attrs = {'cols': '120', 'rows': '10'}
        super().__init__(default_attrs)