import * as React from "react";
import { UserProps, UserState } from "../interfaces/Users";

export class UserFormField extends React.Component<UserProps, UserState> {
    constructor(props: UserProps) {
        super(props);
        this.state = { 
            can_create: props.can_create,
            can_invite: props.can_invite,
            can_manage: props.can_manage
        };

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
        if (active === "True") {
            return "ui button active";
        }
        return "ui button";
    }

    setNoUserPermision(e: any) {
        this.setState(state => ({
            can_create: "False",
            can_invite: "False",
            can_manage: "False"
        }));
    }
    setCreateUserPermission(e: any) {
        this.setState(state => ({
            can_create: "True",
            can_invite: "False",
            can_manage: "False"
        }));
    }
    setInviteUserPermission(e: any) {
        this.setState(state => ({
            can_create: "False",
            can_invite: "True",
            can_manage: "False"
        }));
    }
    setManageUserPermission(e: any) {
        this.setState(state => ({
            can_create: "False",
            can_invite: "False",
            can_manage: "True"
        }));
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
                <input
                    type="hidden"
                    id={this.getIdString("create", this.props.id)}
                    name={this.getNameString("create", this.props.id)}
                    value={String(this.state.can_create)}
                />
                <input
                    type="hidden"
                    id={this.getIdString("invite", this.props.id)}
                    name={this.getNameString("invite", this.props.id)}
                    value={String(this.state.can_invite)}
                />
                <input
                    type="hidden"
                    id={this.getIdString("manage", this.props.id)}
                    name={this.getNameString("manage", this.props.id)}
                    value={String(this.state.can_manage)}
                />
                <div className="ui buttons">
                    <button
                        type="button"
                        className={this.getButtonClass("False")} // TODO: Clearly this is not correct.
                        onClick={this.setNoUserPermision}>
                        <i className="circle slash icon"></i>
                        None
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.state.can_create)}
                        onClick={this.setCreateUserPermission}>
                        <i className="plus icon"></i>
                        Create
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.state.can_invite)}
                        onClick={this.setInviteUserPermission}>
                        <i className="megaphone icon"></i>
                        Invite
                    </button>
                    <button
                        type="button"
                        className={this.getButtonClass(this.state.can_manage)}
                        onClick={this.setManageUserPermission}>
                        <i className="briefcase icon"></i>
                        Manage
                    </button>
                </div>
            </td>
        </tr>;
    }
}
