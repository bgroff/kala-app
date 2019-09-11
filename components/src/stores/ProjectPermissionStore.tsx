import axios from 'axios'
import { action } from 'mobx'
import { PermissionTypes, Permission } from '../components/UserForm';
import { getCSRF } from "../utilities/csrf";
import { PermissionStore, IPermissionStore } from './PermissionStore';


export class ProjectPermissionStore extends PermissionStore implements IPermissionStore {
    private projectId: number;

    init() {
        const path: any[] = window.location.pathname.split('/');
        this.projectId = path[2];
        this.url = '/v1/projects/' + this.projectId + '/permission';
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
        const permissionId: number = this.permissions[userIndex].project ? this.permissions[userIndex].project.id : null;
        this.permissions[userIndex].project = {
            id: permissionId,
            permission: newPermission,
            user_id: id,
            project_id: this.projectId
        } as Permission;
        this.permissions[userIndex].project[newPermission] = true;

        try {
            if (newPermission === PermissionTypes.None) {
                await axios.delete(
                    this.url + "/" + permissionId,
                    {headers: {'X-CSRFToken': getCSRF()}}
                );
                this.permissions[userIndex].project = null;
            }
            else if (permissionId) {
                const response = await axios.put(
                    this.url + "/" + permissionId,
                    this.permissions[userIndex].project,
                    {headers: {'X-CSRFToken': getCSRF()}}
                );
                this.permissions[userIndex].project = response.data.project;
            } else {
                delete this.permissions[userIndex].project.id;
                const response = await axios.post(
                    this.url,
                    this.permissions[userIndex].project,
                    {headers: {'X-CSRFToken': getCSRF()}}
                );
                this.permissions[userIndex].project = response.data.project;
            }
        } catch (error) {
            console.log("failed");
        }
    }
}