from django.forms import ModelForm
from django.db import models
from django import forms

from wammu_web.phonedb.models import Feature

from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe



class SearchForm(forms.Form):
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
