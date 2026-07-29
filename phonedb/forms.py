from django import forms
from django.forms import Form, ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from phonedb.models import Feature, Phone


class SearchForm(Form):
    q = forms.CharField(label=gettext_lazy("Search text"), required=False)
    feature = forms.MultipleChoiceField(
        label=gettext_lazy("Features"),
        required=False,
        choices=(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["feature"].choices = [
            (
                f.name,
                mark_safe(
                    _('%(description)s [<a href="%(url)s">Link</a>]')
                    % {
                        "description": f.get_description(),
                        "url": f"/phones/search/{f.name}/",
                    },
                ),
            )
            for f in Feature.objects.all()
        ]


class NewForm(ModelForm):
    features = forms.MultipleChoiceField(
        label=gettext_lazy("Features"),
        required=False,
        help_text=gettext_lazy("Features which are working in Gammu."),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Phone
        fields = (
            "vendor",
            "name",
            "connection",
            "model",
            "features",
            "gammu_version",
            "note",
            "author_name",
            "author_email",
            "email_garble",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["features"].choices = [
            (
                f.id,
                _("%(description)s (%(name)s)")
                % {"description": f.get_description(), "name": f.name},
            )
            for f in Feature.objects.all()
        ]
