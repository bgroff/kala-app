import { DocumentPermissionStore } from './DocumentPermissionStore'
import { ProjectPermissionStore } from './ProjectPermissionStore';
import { OrganizationPermissionStore } from './OrganizationPermissionStore';

export const stores = {
    documentPermissionStore: new DocumentPermissionStore(),
    projectPermissionStore: new ProjectPermissionStore(),
    organizationPermissionStore: new OrganizationPermissionStore()
}
