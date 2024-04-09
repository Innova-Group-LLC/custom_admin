from django_filters import rest_framework as drf_filters


class ChoiceFilter(drf_filters.ChoiceFilter):

    def __init__(self, *args, **kwargs):
        if callable(kwargs['choices']):
            kwargs['choices'] = kwargs['choices']()

        super().__init__(*args, **kwargs)
