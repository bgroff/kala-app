#from .projects.settings.archive import ArchiveView
from .projects.settings.delete import DeleteView
from .projects.settings.categories import CategoriesView, NewCategoryView, EditCategoryView
from .projects.settings.details import DetailsView
from .projects.settings.manage_access import ManageAccessView
from .projects.settings.transfer_ownership import TransferOwnershipView
from .documents.document import DocumentView
from .documents.new_document import NewDocumentView
from .documents.new_version import NewDocumentVersionView
from .documents.document import DocumentView, ExportDocumentView
from .documents.download import DocumentDownload
from .documents.invite_user import InviteUserView as DocumentInviteUserView
from .documents.settings.details import DocumentDetailsView
from .documents.settings.manage_access import ManageAccessView as DocumentManageAccessView
#from .documents.settings.archive import ArchiveView as DocumentArchiveView
from .documents.settings.delete import DeleteView as DocumentDeleteView
from .documents.settings.transfer_ownership import TransferOwnershipView as DocumentTransferOwnershipView
from .projects.new_project import NewProjectView
from .projects.project import ProjectView, ExportProjectView
from .projects.projects import ProjectsView
from .projects.invite_user import InviteUserView as ProjectInviteUserView
