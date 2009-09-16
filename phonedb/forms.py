from django.forms import ModelForm, Form
from django.db import models
from django import forms

from wammu_web.phonedb.models import Feature, Phone

from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe



class SearchForm(Form):
    q = forms.CharField(label = ugettext_lazy('Search text'), required = False)
    feature = forms.MultipleChoiceField(
        label = ugettext_lazy('Features'),
        required = False,
        choices = [(f.name,
            mark_safe(ugettext_lazy('%s [<a href="%s">Link</a>]') %
                (f.get_description(), '/phone/search/' + f.name))
                ) for f in Feature.objects.all()],
        widget = forms.CheckboxSelectMultiple
        )

class NewForm(ModelForm):
    class Meta:
        model = Phone
        fields = (
            'name',
            'vendor',
            'connection',
            'features',
            'model',
            'gammu_version',
            'note',
            'author_name',
            'author_email',
            'email_garble')

