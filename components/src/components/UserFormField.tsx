import * as React from "react";
import {UserProps} from "./UserForm";

export class UserFormField extends React.Component<UserProps, {}> {
    getIdString(type: string, id: number) {
        return "id_can_" + type + "_" + id;
    }

    getNameString(type: string, id: number) {
        return "can_" + type + "_" + id;
    }

    render() {
        return <span>
            <input
                type="hidden"
                id={this.getIdString("create", this.props.id)}
                name={this.getNameString("create", this.props.id)}
                value={String(this.props.can_create)}
            />
            <input
                type="hidden"
                id={this.getIdString("invite", this.props.id)}
                name={this.getNameString("invite", this.props.id)}
                value={String(this.props.can_invite)}
            />
            <input
                type="hidden"
                id={this.getIdString("manage", this.props.id)}
                name={this.getNameString("manage", this.props.id)}
                value={String(this.props.can_manage)}
            />
        </span>;
    }
}
