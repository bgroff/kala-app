import * as React from "react";

import { UserForm, HigherOrderType } from "./UserForm";
import { inject, observer } from "mobx-react";


@inject('organizationPermissionStore')
@observer
export class OrganizationUserForm extends UserForm {
    componentWillMount() {
        this.permissionStore = this.props.organizationPermissionStore;
        this.permissionStore.init();
        this.permissionStore.fetchPermissions();
        this.higherOrderType = HigherOrderType.Organization;
    }
}
