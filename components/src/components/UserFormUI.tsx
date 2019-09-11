import * as React from "react";
import {UserPermission, PermissionTypes, HigherOrderType} from "./UserForm";


export class UserFormUI extends React.Component<UserPermission, {}> {
    // Keep track of the current permission in case it needs to be reset.
    // This could happen if the network request failed.
    private getCurrentPermission(): PermissionTypes {
        if (this.props.higherOrderType === HigherOrderType.Organization) {
            if (!this.props.organization) return PermissionTypes.None;
            if (this.props.organization.canCreate != null) return PermissionTypes.Create;
            if (this.props.organization.canInvite != null) return PermissionTypes.Invite;
            if (this.props.organization.canManage != null) return PermissionTypes.Manage;
        }
        if (this.props.higherOrderType === HigherOrderType.Project) {
            if (!this.props.project) return PermissionTypes.None;
            if (this.props.project.canCreate != null) return PermissionTypes.Create;
            if (this.props.project.canInvite != null) return PermissionTypes.Invite;
            if (this.props.project.canManage != null) return PermissionTypes.Manage;
        }
        if (this.props.higherOrderType === HigherOrderType.Document) {
            if (!this.props.document) return PermissionTypes.None;
            if (this.props.document.canCreate != null) return PermissionTypes.Create;
            if (this.props.document.canInvite != null) return PermissionTypes.Invite;
            if (this.props.document.canManage != null) return PermissionTypes.Manage;
        }
        return PermissionTypes.None;
    }

    public getButtonClass(permission: PermissionTypes) {
        if (this.props.higherOrderType === HigherOrderType.Organization) {
            if (!this.props.organization) return PermissionTypes.None === permission ? "ui button active" : "ui button";
            if (PermissionTypes.Create === permission && this.props.organization.canCreate != null) return "ui button active";
            if (PermissionTypes.Invite === permission && this.props.organization.canInvite != null) return "ui button active";
            if (PermissionTypes.Manage === permission && this.props.organization.canManage != null) return "ui button active"; 
        }
        if (this.props.higherOrderType === HigherOrderType.Project) {
            if (!this.props.project) return PermissionTypes.None === permission ? "ui button active" : "ui button";
            if (PermissionTypes.Create === permission && this.props.project.canCreate != null) return "ui button active";
            if (PermissionTypes.Invite === permission && this.props.project.canInvite != null) return "ui button active";
            if (PermissionTypes.Manage === permission && this.props.project.canManage != null) return "ui button active"; 
        }
        if (this.props.higherOrderType === HigherOrderType.Document) {
            if (!this.props.document) return PermissionTypes.None === permission ? "ui button active" : "ui button";
            if (PermissionTypes.Create === permission && this.props.document.canCreate != null) return "ui button active";
            if (PermissionTypes.Invite === permission && this.props.document.canInvite != null) return "ui button active";
            if (PermissionTypes.Manage === permission && this.props.document.canManage != null) return "ui button active"; 
        }
        return "ui button";
    }

    getExtraContent() {
        var returnString: JSX.Element;
        if (this.props.higherOrderType === HigherOrderType.Document) {
            if (this.props.organization) {
                if (this.props.organization.canCreate) return <i className="circular organization icon link" data-content="This user has organization create permissions" data-variation="tiny"></i>;
                if (this.props.organization.canInvite) return <i className="circular organization icon link" data-content="This user has organization invite permissions" data-variation="tiny"></i>;
                if (this.props.organization.canManage) return <i className="circular organization icon link" data-content="This user has organization manage permissions" data-variation="tiny"></i>;

            }
            if (this.props.project) {
                if (this.props.project.canCreate) return <i className="circular checklist icon link" data-content="This user has project create permissions" data-variation="tiny"></i>;
                if (this.props.project.canInvite) return <i className="circular checklist icon link" data-content="This user has project invite permissions" data-variation="tiny"></i>;
                if (this.props.project.canManage) return <i className="circular checklist icon link" data-content="This user has project manage permissions" data-variation="tiny"></i>;
            }
        }
        if (this.props.higherOrderType === HigherOrderType.Project) {
            if (this.props.organization) {
                if (this.props.organization.canCreate) return <i className="circular organization icon link" data-content="This user has organization create permissions" data-variation="tinu"></i>;
                if (this.props.organization.canInvite) return <i className="circular organization icon link" data-content="This user has organization invite permissions" data-variation="tiny"></i>;
                if (this.props.organization.canManage) return <i className="circular organization icon link" data-content="This user has organization manage permissions" data-variation="tiny"></i>;

            }
        }

        return returnString;
    }

    setPermision = (permission: PermissionTypes): void  => {
        this.props.onPermissionChange(this.props.user.id, permission, this.getCurrentPermission());
    }

    render() {
        return <tr>
            <td>
                <h4 className="ui header">
                    <div className="content">
                        <span className="ui tooltip">{this.getExtraContent()}</span>
                        {this.props.user.lastName + ", " + this.props.user.firstName}
                    </div>
                </h4>
            </td>
            <td>
            </td><td>
                <div className="ui buttons">
                    <button
                        type="button"
                        className={this.getButtonClass(PermissionTypes.None)}
                        onClick={() => this.setPermision(PermissionTypes.None)}>
                        <i className="circle slash icon"></i>
                        None
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(PermissionTypes.Create)}
                        onClick={() => this.setPermision(PermissionTypes.Create)}>
                        <i className="plus icon"></i>
                        Create
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(PermissionTypes.Invite)}
                        onClick={() => this.setPermision(PermissionTypes.Invite)}>
                        <i className="megaphone icon"></i>
                        Invite
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(PermissionTypes.Manage)}
                        onClick={() => this.setPermision(PermissionTypes.Manage)}>
                        <i className="briefcase icon"></i>
                        Manage
                    </button>
                </div>
            </td>
        </tr>;
    }
}
