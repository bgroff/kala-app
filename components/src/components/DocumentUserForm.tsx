import { UserForm } from "./UserForm";
import { inject, observer } from "mobx-react";


@inject('documentPermissionStore')
@observer
export class DocumentUserForm extends UserForm {
    componentWillMount() {
        this.permissionStore = this.props.documentPermissionStore;
        this.permissionStore.init();
        this.permissionStore.fetchPermissions()

    }
}
