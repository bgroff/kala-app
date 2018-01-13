from .projects.settings.category import CategoryForm
from .projects.settings.details import DetailsForm
from .projects.settings.manage_access import ManageAccessForm, manage_access_forms
from .projects.settings.transfer_ownership import TransferOwnershipForm
from .projects.new_project import NewProjectForm


from django import forms
from documents.defs import get_categories_for_mimes
from documents.models import Document

#
# class SortCategoryForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         self.project = kwargs.pop('project')
#         super(CategoryForm, self).__init__(*args, **kwargs)
#
#         self.fields['category'] = forms.ChoiceField(choices=get_categories_for_mimes(
#             Document.objects.active().filter(project=self.project).distinct('mime').order_by('mime').values_list(
#                 'mime')), widget=forms.Select(attrs={'class': 'span3'}))
#

class SortForm(forms.Form):
    sort = forms.ChoiceField(choices=(('Date', 'Sort by Date'), ('Alphabetically', 'Sort Alphabetically')),
                               widget=forms.RadioSelect,
                               initial='Date')
