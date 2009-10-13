from django.forms import ModelForm, Form
from django.db import models
from django import forms

from phonedb.models import Feature, Phone

from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe



class SearchForm(Form):
    q = forms.CharField(label = ugettext_lazy('Search text'), required = False)
    feature = forms.MultipleChoiceField(
        label = ugettext_lazy('Features'),
        required = False,
        choices = [(f.name,
            mark_safe(ugettext_lazy('%(description)s [<a href="%(url)s">Link</a>]') %
                {'description': f.get_description(), 'url': '/phones/search/%s/' % f.name})
                ) for f in Feature.objects.all()],
        widget = forms.CheckboxSelectMultiple
        )

class NewForm(ModelForm):
    features = forms.MultipleChoiceField(
        label = ugettext_lazy('Features'),
        required = False,
        help_text = ugettext_lazy('Features which are working in Gammu.'),
        choices = [(f.id,
            ugettext_lazy('%(description)s (%(name)s)') %
                {'description': f.get_description(), 'name': f.name}
                ) for f in Feature.objects.all()],
        widget = forms.CheckboxSelectMultiple
        )

    class Meta:
        model = Phone
        fields = (
            'vendor',
            'name',
            'connection',
            'model',
            'features',
            'gammu_version',
            'note',
            'author_name',
            'author_email',
            'email_garble')
