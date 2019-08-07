import axios from 'axios'
import { action, computed, observable } from 'mobx'
import { PermissionTypes, UserPermission } from '../components/UserForm';


export interface IDocumentPermissionStore {
    error: any;
    isFetching: boolean;
    userPermissions: UserPermission[];
    numberOfPages: number;
    activePage: number;

    fetchDocumentPermissions(projectId: number, documentId: number): void;
    setPermission(id: number, permission: PermissionTypes): boolean;
    setActivePage(activePage: number): number;
    setFilter(filter: string): string;
    setSearch(search: string): string;
}

export class DocumentPermissionStore implements IDocumentPermissionStore {
    @observable error: any = null;
    @observable isFetching = false;
    @observable permissions: UserPermission[] = [];
    @observable permissionsPerPage: number = 30;
    @observable currentPage: number = 1;
    @observable search: string = "";
    @observable filter: string = "no_filter";
    user: UserPermission;

    @action async fetchDocumentPermissions(projectId: number, documentId: number) {
        this.isFetching = true;
        this.error = null;
        try {
            const response = await axios.get('/v1/projects/' + projectId + '/documents/' + documentId + '/permission');
            this.permissions = response.data;
            this.isFetching = false;
        } catch (error) {
            this.error = error;
            this.isFetching = false;
        }
    }

    @computed get numberOfPages(): number {
        return Math.ceil(this.permissions.length / this.permissionsPerPage);
    }


    @computed get activePage(): number  {
        return this.currentPage;
    }

    @action setActivePage(activePage: number): number  {
        this.currentPage = activePage;
        return this.currentPage;
    }

    @computed get userPermissions(): UserPermission[] {
        let filteredUsers: UserPermission[] = this.permissions;
        console.log("Computing userPermissions");
        if (this.search != "") {
            filteredUsers = filteredUsers.filter(user => user.user.lastName.toLowerCase().startsWith(this.search.toLowerCase()));
        }

        if (this.filter === null) {
            filteredUsers = filteredUsers.filter(user => user.document === undefined);
        } else if (this.filter === "can_create") {
            filteredUsers = filteredUsers.filter(user => user.document.canCreate === true);
        } else if (this.filter === "can_invite") {
            filteredUsers = filteredUsers.filter(user => user.document.canInvite === true);
        } else if (this.filter === "can_manage") {
            filteredUsers = filteredUsers.filter(user => user.document.canManage === true);
        }

        let offset = Math.ceil((this.currentPage - 1) * this.permissionsPerPage);
        console.log(filteredUsers.slice(offset, offset + this.permissionsPerPage));
        return filteredUsers.slice(offset, offset + this.permissionsPerPage);
    }

    @action setFilter(filter: string) {
        this.filter = filter;
        return this.filter;
    }

    @action setSearch(search: string) {
        this.search = search;
        return this.search;
    }

    @action setPermission = (id: number, permission: PermissionTypes): boolean => {
        const userIndex = this.permissions.findIndex(user => user.user.id = id);
        switch (permission) {
            case PermissionTypes.None:  {
                this.permissions[userIndex].document = {
                    id: this.permissions[userIndex].document ? this.permissions[userIndex].document.id : null,
                };
                break;
            }
            case PermissionTypes.Create: {
                this.permissions[userIndex].document = {
                    id: this.permissions[userIndex].document ? this.permissions[userIndex].document.id : null,
                    canCreate: true
                };
                break;
            }
            case PermissionTypes.Invite: {
                this.permissions[userIndex].document = {
                    id: this.permissions[userIndex].document ? this.permissions[userIndex].document.id : null,
                    canInvite: true
                };
                break;
            }
            case PermissionTypes.Manage: {
                this.permissions[userIndex].document = {
                    id: this.permissions[userIndex].document ? this.permissions[userIndex].document.id : null,
                    canManage: true
                };
                break;
            }
            default: break;
        }
        return true;
    }
}