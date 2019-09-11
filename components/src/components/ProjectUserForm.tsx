import { UserForm, HigherOrderType } from "./UserForm";
import { inject, observer } from "mobx-react";


@inject('projectPermissionStore')
@observer
export class ProjectUserForm extends UserForm {
    componentWillMount() {
        this.permissionStore = this.props.projectPermissionStore;
        this.permissionStore.init();
        this.permissionStore.fetchPermissions();
        this.higherOrderType = HigherOrderType.Project;
    }
}
