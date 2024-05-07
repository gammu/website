from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
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
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.layout = Layout(
            "q",
            "feature",
            Submit("submit", _("Search"), css_class="btn-default"),
        )
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
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.layout = Layout(
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
            Submit("submit", gettext_lazy("Save"), css_class="btn-default"),
        )
        self.fields["features"].choices = [
            (
                f.id,
                _("%(description)s (%(name)s)")
                % {"description": f.get_description(), "name": f.name},
            )
            for f in Feature.objects.all()
        ]
