import axios from 'axios'
import { action, computed, observable } from 'mobx'
import { PermissionTypes, UserPermission, Permission } from '../components/UserForm';
import { getCSRF } from "../utilities/csrf";

export interface IDocumentPermissionStore {
    error: any;
    isFetching: boolean;
    userPermissions: UserPermission[];
    numberOfPages: number;
    activePage: number;

    init(projectId: number, documentId: number): void;
    fetchDocumentPermissions(): void;
    setPermission(id: number, newPermission: PermissionTypes, oldPermission: PermissionTypes): void;
    setActivePage(activePage: number): number;
    setFilter(filter: string): string;
    setSearch(search: string): string;
}

export class DocumentPermissionStore implements IDocumentPermissionStore {
    private url: string;
    private projectId: number;
    private documentId: number;

    @observable error: any = null;
    @observable isFetching = false;
    @observable permissions: UserPermission[] = [];
    @observable permissionsPerPage: number = 30;
    @observable currentPage: number = 1;
    @observable search: string = "";
    @observable filter: string = "no_filter";
    user: UserPermission;

    init(projectId: number, documentId: number) {
        console.log(window.location.pathname);
        this.projectId = projectId;
        this.documentId = documentId;
        this.url = '/v1/projects/' + projectId + '/documents/' + documentId + '/permission';
    }

    @action async fetchDocumentPermissions() {
        this.isFetching = true;
        this.error = null;
        try {
            const response = await axios.get(this.url);
            this.permissions = response.data;
            this.isFetching = false;
        } catch (error) {
            this.error = error;
            this.isFetching = false;
        }
    }

    @computed get numberOfPages(): number {
        return Math.ceil(this.filteredUsers.length / this.permissionsPerPage);
    }


    @computed get activePage(): number  {
        if (this.numberOfPages < this.currentPage) {
            return this.numberOfPages;
        }
        return this.currentPage;
    }

    @action setActivePage(activePage: number): number  {
        this.currentPage = activePage;
        return this.currentPage;
    }


    @computed get filteredUsers(): UserPermission[] {
        let filteredUsers: UserPermission[] = this.permissions;
        if (this.search != "") {
            filteredUsers = filteredUsers.filter(user => user.user.lastName.toLowerCase().startsWith(this.search.toLowerCase()));
        }

        if (this.filter === PermissionTypes.None) {
            filteredUsers = filteredUsers.filter(user => user.document === undefined);
        } else if (this.filter === PermissionTypes.Create) {
            filteredUsers = filteredUsers.filter(user => 
                (user.document && user.document.canCreate === true) ||
                (user.project && user.project.canCreate === true) ||
                (user.organization && user.organization.canCreate === true));
        } else if (this.filter === PermissionTypes.Invite) {
            filteredUsers = filteredUsers.filter(user => 
                (user.document && user.document.canInvite === true) ||
                (user.project && user.project.canInvite === true) ||
                (user.organization && user.organization.canInvite === true));
        } else if (this.filter === PermissionTypes.Manage) {
            filteredUsers = filteredUsers.filter(user =>
                (user.document && user.document.canManage === true) ||
                (user.project && user.project.canManage === true) ||
                (user.organization && user.organization.canManage === true));
        }
        return filteredUsers;
    }

    @computed get userPermissions(): UserPermission[] {
        let offset = Math.ceil((this.activePage - 1) * this.permissionsPerPage);
        return this.filteredUsers.slice(offset, offset + this.permissionsPerPage);
    }

    @action setFilter(filter: string) {
        this.filter = filter;
        return this.filter;
    }

    @action setSearch(search: string) {
        this.search = search;
        return this.search;
    }

    /**
     * setPermission updates the users permission in the [[permissions]] array and then sends
     * the request to the backend for action. If the backend is not successful then the old permission
     * is reset.
     * 
     * [[userIndex]] is the actioned user, this users permission is then replaced with the [[newPermission]].
     * If the id is present in the permission object, then that user already has a permission. If this is the 
     * case then an put or delete can occur, otherwise the data must be posted to the endpoint.
     */
    @action async setPermission(id: number, newPermission: PermissionTypes, oldPermission: PermissionTypes) {
        const userIndex: number = this.permissions.findIndex(user => user.user.id === id);
        const permissionId: number = this.permissions[userIndex].document ? this.permissions[userIndex].document.id : null;
        this.permissions[userIndex].document = {
            id: permissionId,
            permission: newPermission,
            user_id: id,
            document_id: this.documentId
        } as Permission;
        this.permissions[userIndex].document[newPermission] = true;

        try {
            if (newPermission === PermissionTypes.None) {
                await axios.delete(
                    this.url + "/" + permissionId,
                    {headers: {'X-CSRFToken': getCSRF()}}
                );
                this.permissions[userIndex].document = null;
            }
            else if (permissionId) {
                const response = await axios.put(
                    this.url + "/" + permissionId,
                    this.permissions[userIndex].document,
                    {headers: {'X-CSRFToken': getCSRF()}}
                );
                this.permissions[userIndex].document = response.data.document;
            } else {
                delete this.permissions[userIndex].document.id;
                const response = await axios.post(
                    this.url,
                    this.permissions[userIndex].document,
                    {headers: {'X-CSRFToken': getCSRF()}}
                );
                this.permissions[userIndex].document = response.data.document;
            }
        } catch (error) {
            console.log("failed");
        }
    }
}