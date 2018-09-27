from .projects.settings.category import CategoryForm
from .projects.settings.details import DetailsForm
from auth.forms.manage_access import manage_access_forms
from .projects.settings.transfer_ownership import TransferOwnershipForm
from .projects.new_project import NewProjectForm


from django import forms

class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=(('Date', 'Sort by Date'), ('Alphabetically', 'Sort Alphabetically')),
                               widget=forms.RadioSelect,
                               initial='Date')
