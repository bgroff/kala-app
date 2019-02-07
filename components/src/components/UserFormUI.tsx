import * as React from "react";
import {UserProps} from "./UserForm";


export class UserFormUI extends React.Component<UserProps, {}> {
    constructor(props: UserProps) {
        super(props);

        this.setNoUserPermision = this.setNoUserPermision.bind(this);
        this.setCreateUserPermission = this.setCreateUserPermission.bind(this);
        this.setInviteUserPermission = this.setInviteUserPermission.bind(this);
        this.setManageUserPermission = this.setManageUserPermission.bind(this);
    }

    getIdString(type: string, id: number) {
        return "id_can_" + type + "_" + id;
    }

    getNameString(type: string, id: number) {
        return "can_" + type + "_" + id;
    }

    getButtonClass(active: string) {
        if (active === "None") {
            return this.props.can_create === "True" ||
                this.props.can_invite === "True" ||
                this.props.can_manage === "True" ? "ui button" : "ui button active";
        }
        if (active === "True") {
            return "ui button active";
        }
        return "ui button";
    }

    setNoUserPermision(e: any) {
        this.props.onPermissionChange(this.props.id, {
            can_create: "False",
            can_invite: "False",
            can_manage: "False",
            state: "none",
        });
    }
    setCreateUserPermission(e: any) {
        this.setState(state => this.props.onPermissionChange(this.props.id, {
            can_create: "True",
            can_invite: "False",
            can_manage: "False",
            state: "can_create",
        }));
    }
    setInviteUserPermission(e: any) {
        this.props.onPermissionChange(this.props.id, {
            can_create: "False",
            can_invite: "True",
            can_manage: "False",
            state: "can_invite",
        });
    }
    setManageUserPermission(e: any) {
        this.props.onPermissionChange(this.props.id, {
            can_create: "False",
            can_invite: "False",
            can_manage: "True",
            state: "can_manage",
        });
    }

    render() {
        return <tr>
            <td>
                <h4 className="ui header">
                    <div className="content">
                        {this.props.name}
                    </div>
                </h4>
            </td>
            <td>
            </td><td>
                <div className="ui buttons">
                    <button
                        type="button"
                        className={this.getButtonClass("None")}
                        onClick={this.setNoUserPermision}>
                        <i className="circle slash icon"></i>
                        None
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.props.can_create)}
                        onClick={this.setCreateUserPermission}>
                        <i className="plus icon"></i>
                        Create
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.props.can_invite)}
                        onClick={this.setInviteUserPermission}>
                        <i className="megaphone icon"></i>
                        Invite
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.props.can_manage)}
                        onClick={this.setManageUserPermission}>
                        <i className="briefcase icon"></i>
                        Manage
                    </button>
                </div>
            </td>
        </tr>;
    }
}
