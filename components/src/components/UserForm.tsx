import * as React from "react";
import { UserFormField } from "./UserFormField";
import { UserFormUI } from "./UserFormUI";
import ReactPaginate from 'react-paginate';

export interface UserProps {
    name: string,
    id: number,
    can_create: string,
    can_invite: string,
    can_manage: string,
    onPermissionChange: (key: number, permissions: object) => object
}

export interface UsersProps extends Array<UserProps> { }
export interface UsersList { users: UsersProps }
export interface FormState { users: any, numberOfPages: number, pagedUsers: UsersProps }
const usersPerPage: number = 10;

export class UserForm extends React.Component<UsersList, FormState> {
    constructor(props: UsersList) {
        super(props);
        this.state = {
            numberOfPages: Math.ceil(props.users.length / usersPerPage),
            pagedUsers: this.props.users.slice(0, usersPerPage),
            users: this.props.users.reduce((users: any, user: UserProps) => {
                users[user.id] = {
                    can_create: user.can_create,
                    can_invite: user.can_invite,
                    can_manage: user.can_manage
                }
                return users
            }, {}),
        };

        this.setUserPermissions = this.setUserPermissions.bind(this);
        this.handlePageClick = this.handlePageClick.bind(this);
    }

    setUserPermissions(key: number, permissions: object) {
        this.setState(state => state.users[key] = permissions)

        return permissions;
    }

    handlePageClick(data: any) {
        let selected = data.selected;
        let offset = Math.ceil(selected * usersPerPage);
        this.setState({ pagedUsers: this.props.users.slice(offset, offset + usersPerPage) });
    };

    render() {
        return <span>
            {this.props.users.map(user => <UserFormField key={user.id}
                name={user.name}
                id={user.id}
                can_create={this.state.users[user.id].can_create}
                can_invite={this.state.users[user.id].can_invite}
                can_manage={this.state.users[user.id].can_manage}
                onPermissionChange={this.setUserPermissions} />)}
            <table className="ui very basic table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th></th>
                        <th>Manage acess</th>
                    </tr>
                </thead>

                <tbody>
                    {this.state.pagedUsers.map(user => <UserFormUI
                        key={user.id}
                        name={user.name}
                        id={user.id}
                        can_create={this.state.users[user.id].can_create}
                        can_invite={this.state.users[user.id].can_invite}
                        can_manage={this.state.users[user.id].can_manage}
                        onPermissionChange={this.setUserPermissions} />)}
                </tbody>
            </table>
            <ReactPaginate
                previousLabel={'previous'}
                nextLabel={'next'}
                breakLabel={'...'}
                breakClassName={'break-me'}
                pageCount={this.state.numberOfPages}
                marginPagesDisplayed={2}
                pageRangeDisplayed={5}
                onPageChange={this.handlePageClick}
                containerClassName={'ui pagination menu'}
                pageLinkClassName={'item'}
                activeClassName={'active'}
            />
        </span>;
    }
}