import axios from 'axios'
import { action } from 'mobx'
import { PermissionTypes, Permission } from '../components/UserForm';
import { getCSRF } from "../utilities/csrf";
import { PermissionStore, IPermissionStore } from './PermissionStore';


export class DocumentPermissionStore extends PermissionStore implements IPermissionStore {
    private projectId: number;
    private documentId: number;

    init() {
        const path: any[] = window.location.pathname.split('/');
        this.projectId = path[2];
        this.documentId = path[3];
        this.url = '/v1/projects/' + this.projectId + '/documents/' + this.documentId + '/permission';
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