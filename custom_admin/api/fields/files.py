import base64
import io
import sys
import urllib

from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.forms import FileField as DjangoFileField
from django.utils.translation import gettext as _
from rest_framework import fields, serializers


class Base64Serializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    file = serializers.CharField(required=False)

    def validate_file(self, file):
        if not file.startswith('data:image'):
            raise ValidationError('Bad base64 format')
        return file


class Base64FileField(fields.FileField):
    list_preview: bool = False

    def __init__(self, *args, **kwargs):
        self.list_preview = kwargs.pop('list_preview', False)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if not data:
            return

        serializer = Base64Serializer(data=data)
        serializer.is_valid(raise_exception=True)

        content_type, base64_str = serializer.validated_data['file'].split(",")
        upload_file = io.BytesIO(base64.b64decode(base64_str))
        file_object = UploadedFile(
            file=upload_file,
            name=serializer.validated_data['name'],
            content_type=content_type,
            size=sys.getsizeof(upload_file),
        )
        return super().to_internal_value(file_object)

    def to_representation(self, file):
        url = super().to_representation(file)
        if not url:
            return url

        request = self.context['request']
        url = urllib.parse.unquote(request.build_absolute_uri(url))
        return {
            'name': file.name,
            'url': url,
        }


def validate_image_file_extension(value):
    additional = ['svg']
    return validators.FileExtensionValidator(
        allowed_extensions=validators.get_available_image_extensions() + additional
    )(value)


class SVGDjangoFileField(DjangoFileField):
    default_validators = [validate_image_file_extension]

    def to_python(self, data):
        from PIL import Image

        f = super().to_python(data)
        if f is None:
            return None

        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                file = io.BytesIO(data.read())
            else:
                file = io.BytesIO(data['content'])

        if not data.name.endswith('.svg'):
            try:
                image = Image.open(file)
                image.verify()

                f.image = image
                f.content_type = Image.MIME.get(image.format)
            except Exception as exc:
                print(exc)
                raise ValidationError(
                    self.error_messages['invalid_image'],
                    code='invalid_image',
                ) from exc

        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f


class Base64ImageField(Base64FileField, fields.FileField):
    default_error_messages = {
        'invalid_image': _(
            'Загрузите корректное изображение. Загруженный файл либо не является изображением, либо поврежден.'
        ),
    }

    def to_internal_value(self, data):
        file_object = super().to_internal_value(data)
        django_field = SVGDjangoFileField()
        django_field.error_messages = self.error_messages
        return django_field.clean(file_object)


class SVGField(serializers.CharField):
    ''' For raw html '''
