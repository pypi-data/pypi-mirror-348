from django.conf import settings
from rest_framework.serializers import BooleanField as DRFBooleanField
from rest_framework.serializers import CharField as DRFCharField
from rest_framework.serializers import ChoiceField as DRFChoiceField
from rest_framework.serializers import DateField as DRFDateField
from rest_framework.serializers import DateTimeField as DRFDateTimeField
from rest_framework.serializers import DecimalField as DRFDecimalField
from rest_framework.serializers import DictField as DRFDictField
from rest_framework.serializers import DurationField as DRFDurationField
from rest_framework.serializers import EmailField as DRFEmailField
from rest_framework.serializers import Field as DRFField
from rest_framework.serializers import FileField as DRFFileField
from rest_framework.serializers import FilePathField as DRFFilePathField
from rest_framework.serializers import FloatField as DRFFloatField
from rest_framework.serializers import HStoreField as DRFHStoreField
from rest_framework.serializers import HiddenField as DRFHiddenField
from rest_framework.serializers import IPAddressField as DRFIPAddressField
from rest_framework.serializers import ImageField as DRFImageField
from rest_framework.serializers import IntegerField as DRFIntegerField
from rest_framework.serializers import JSONField as DRFJSONField
from rest_framework.serializers import ListField as DRFListField
from rest_framework.serializers import ModelField as DRFModelField
from rest_framework.serializers import MultipleChoiceField as DRFMultipleChoiceField
from rest_framework.serializers import ReadOnlyField as DRFReadOnlyField
from rest_framework.serializers import RegexField as DRFRegexField
from rest_framework.serializers import SerializerMethodField as DRFSerializerMethodField
from rest_framework.serializers import SlugField as DRFSlugField
from rest_framework.serializers import TimeField as DRFTimeField
from rest_framework.serializers import URLField as DRFURLField
from rest_framework.serializers import UUIDField as DRFUUIDField


class Field(DRFField):

    def __init__(self, error_help_text='', *args, **kwargs):

        if "error_help_text" in kwargs and not kwargs.get('help_text'):
            kwargs["help_text"] = kwargs["error_help_text"]
        super().__init__(*args, **kwargs)
        kwargs["error_help_text"] = error_help_text
        if settings.LANGUAGE_CODE == 'zh-hans':
            if 'error_messages' not in kwargs:
                help_text = kwargs.get('error_help_text') or ''
                if not help_text:
                    help_text = kwargs.get('help_text') or ''
                help_text = f'{help_text}:' if help_text else help_text
                for key in self.error_messages:
                    if key == 'null':
                        self.error_messages['null'] = f'{help_text}不能为空。'
                    elif key == 'blank':
                        self.error_messages['blank'] = f'{help_text}不能为空白。'
                    else:
                        self.error_messages[key] = f'{help_text}{self.error_messages[key]}'


class BooleanField(Field, DRFBooleanField): pass


class CharField(Field, DRFCharField):

    def __init__(self, **kwargs):
        if "allow_blank" not in kwargs:
            kwargs["allow_blank"] = True
        super().__init__(**kwargs)


class ChoiceField(Field, DRFChoiceField): pass


class DateField(Field, DRFDateField): pass


class DateTimeField(Field, DRFDateTimeField): pass


class DecimalField(Field, DRFDecimalField): pass


class DictField(Field, DRFDictField): pass


class DurationField(Field, DRFDurationField): pass


class EmailField(Field, DRFEmailField): pass


class Field(Field, DRFField): pass


class FileField(Field, DRFFileField): pass


class FilePathField(Field, DRFFilePathField): pass


class FloatField(Field, DRFFloatField): pass


class HiddenField(Field, DRFHiddenField): pass


class HStoreField(Field, DRFHStoreField): pass


class IPAddressField(Field, DRFIPAddressField): pass


class ImageField(Field, DRFImageField): pass


class IntegerField(Field, DRFIntegerField): pass


class JSONField(Field, DRFJSONField): pass


class ListField(Field, DRFListField): pass


class ModelField(Field, DRFModelField): pass


class MultipleChoiceField(Field, DRFMultipleChoiceField): pass


class ReadOnlyField(Field, DRFReadOnlyField): pass


class RegexField(Field, DRFRegexField): pass


class SerializerMethodField(Field, DRFSerializerMethodField): pass


class SlugField(Field, DRFSlugField): pass


class TimeField(Field, DRFTimeField): pass


class URLField(Field, DRFURLField): pass


class UUIDField(Field, DRFUUIDField): pass
