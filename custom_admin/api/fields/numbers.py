from rest_framework.fields import DecimalField, IntegerField


class PositiveIntegerField(IntegerField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_value = 0


class PositiveDecimalField(DecimalField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_value = 0.0
