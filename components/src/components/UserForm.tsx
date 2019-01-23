import * as React from "react";
import { UserFormField } from "./UserFormField";
import { UsersList, FormState } from "../interfaces/Users";

export class UserForm extends React.Component<UsersList, FormState> {
    constructor(props: UsersList) {
        super(props);
        this.state = {
            csrf_token: "rRKoOsRV5Zs1Wbx2swS4U7GUgsDhOfm5iRckHUbInCxd4naArJ284oPlZv4aORGA"
        }
    }

    render() {
        return <table className="ui very basic table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Manage acess</th>
                    </tr>
                </thead>

                <tbody>
                    {this.props.users.map(user => <UserFormField
                        key={user.id}
                        name={user.name}
                        id={user.id}
                        can_create={user.can_create}
                        can_invite={user.can_invite}
                        can_manage={user.can_manage} />)}
                </tbody>
            </table>
    }
}