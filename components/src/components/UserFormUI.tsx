import * as React from "react";
import {UserPermission, PermissionTypes} from "./UserForm";


export class UserFormUI extends React.Component<UserPermission, {}> {

    getButtonClass(active: boolean) {
        return active ? "ui button active" : "ui button";
    }

    setPermision = (permission: PermissionTypes): void  => {
        this.props.onPermissionChange(this.props.user.id, permission);
    }

    render() {
        return <tr>
            <td>
                <h4 className="ui header">
                    <div className="content">
                        {this.props.user.firstName + " " + this.props.user.lastName}
                    </div>
                </h4>
            </td>
            <td>
            </td><td>
                <div className="ui buttons">
                    <button
                        type="button"
                        className={this.getButtonClass(this.props.document ? 
                            !this.props.document.canCreate &&
                            !this.props.document.canInvite &&
                            !this.props.document.canManage : true)}
                        onClick={() => this.setPermision(PermissionTypes.None)}>
                        <i className="circle slash icon"></i>
                        None
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.props.document ? this.props.document.canCreate : false)}
                        onClick={() => this.setPermision(PermissionTypes.Create)}>
                        <i className="plus icon"></i>
                        Create
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.props.document ? this.props.document.canInvite : false)}
                        onClick={() => this.setPermision(PermissionTypes.Invite)}>
                        <i className="megaphone icon"></i>
                        Invite
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.props.document ? this.props.document.canManage: false)}
                        onClick={() => this.setPermision(PermissionTypes.Manage)}>
                        <i className="briefcase icon"></i>
                        Manage
                    </button>
                </div>
            </td>
        </tr>;
    }
}
