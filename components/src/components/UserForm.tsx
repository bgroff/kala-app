import * as React from "react";
import { UserFormField } from "./UserFormField";
import { UserFormUI } from "./UserFormUI";
import { Dropdown, Input, Pagination } from 'semantic-ui-react'


export interface UserProps {
    name: string,
    id: number,
    can_create: string,
    can_invite: string,
    can_manage: string,
    state: string,
    onPermissionChange: (key: number, permissions: object) => object
}

export interface UserFilterDropdown {
    onFilterChange: (event: any, data: any) => void
}

export interface UserNameFilter {
    onNameChange: (event: any, data: any) => void
}

export interface UsersProps extends Array<UserProps> { }
export interface UsersList { users: UsersProps }
export interface FormState { 
    users: any,
    numberOfPages: number,
    activePage: number,
    pagedUsers: UsersProps,
    filteredUsers: UsersProps
    filter: string,
    search: string,
}
const usersPerPage: number = 10;


export class UserNameFilterInput extends React.Component<UserNameFilter, {}> {
    render() {
        return <Input
            placeholder='Search'
            onChange={this.props.onNameChange}
        />
    }
}

const options = [
    { key: 0, text: "No filter", value: "no_filter" },
    { key: 1, text: "No permissions", value: "none" },
    { key: 2, text: "Create permissions", value: "can_create" },
    { key: 3, text: "Invite permissions", value: "can_invite" },
    { key: 4, text: "Manage permissions", value: "can_manage" },
]
export class UserFilterDropdownMenu extends React.Component<UserFilterDropdown, {}> {
    render() {
        return <Dropdown
            placeholder='Filter users'
            selection
            onChange={this.props.onFilterChange}
            options={options}
        />
    }
}

export class UserForm extends React.Component<UsersList, FormState> {
    constructor(props: UsersList) {
        super(props);
        this.state = {
            numberOfPages: Math.ceil(props.users.length / usersPerPage),
            pagedUsers: this.props.users.slice(0, usersPerPage),
            filteredUsers: this.props.users,
            filter: "no_filter",
            search: "",
            activePage: 1,
            users: this.props.users.reduce((users: any, user: UserProps) => {
                users[user.id] = {
                    can_create: user.can_create,
                    can_invite: user.can_invite,
                    can_manage: user.can_manage,
                    state: user.state,
                }
                return users
            }, {}),
        };

        this.setUserPermissions = this.setUserPermissions.bind(this);
        this.handlePaginationChange = this.handlePaginationChange.bind(this);
        this.onFilterChange = this.onFilterChange.bind(this);
        this.onNameChange = this.onNameChange.bind(this);

    }

    setUserPermissions(key: number, permissions: object) {
        this.setState(state => state.users[key] = permissions)

        return permissions;
    }

    filterUsers(filter: string, search: string) {
        let filteredUsers = this.props.users;

        if (search != "") {
            filteredUsers = filteredUsers.filter(user => user.name.toLowerCase().startsWith(search.toLowerCase()));
        }

        if (filter === "none") {
            filteredUsers = filteredUsers.filter(user => user.state === "none");
        } else if (filter === "can_create") {
            filteredUsers = filteredUsers.filter(user => user.state === "can_create");            
        } else if (filter === "can_invite") {
            filteredUsers = filteredUsers.filter(user => user.state === "can_invite");
        } else if (filter === "can_manage") {
            filteredUsers = filteredUsers.filter(user => user.state === "can_manage");
        }

        this.setState({
            filteredUsers: filteredUsers,
            pagedUsers: filteredUsers.slice(0, usersPerPage),
            activePage: 1,
            numberOfPages: Math.ceil(filteredUsers.length / usersPerPage),
            filter: filter,
            search: search
        });

    }

    onFilterChange(event: any, data: any) {
        this.filterUsers(data.value, this.state.search);
    }

    onNameChange(event: any, data: any) {
        this.filterUsers(this.state.filter, data.value);
    }

    handlePaginationChange(event: any, data: any) {
        let activePage = data.activePage;
        let offset = Math.ceil((activePage - 1) * usersPerPage);
        this.setState({
            pagedUsers: this.state.filteredUsers.slice(offset, offset + usersPerPage),
            activePage: activePage
        });
    };

    render() {
        return <span>
            {this.props.users.map(user => <UserFormField key={user.id}
                name={user.name}
                id={user.id}
                can_create={this.state.users[user.id].can_create}
                can_invite={this.state.users[user.id].can_invite}
                can_manage={this.state.users[user.id].can_manage}
                state={this.state.users[user.id].state}
                onPermissionChange={this.setUserPermissions} />)}
            <div className="repo title">
                <div className="repo options">
                    <UserFilterDropdownMenu onFilterChange={this.onFilterChange} />
                </div>
                <UserNameFilterInput onNameChange={this.onNameChange} />
            </div>
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
                        state={this.state.users[user.id].state}
                        onPermissionChange={this.setUserPermissions} />)}
                </tbody>
            </table>
            <Pagination
                activePage={this.state.activePage}
                totalPages={this.state.numberOfPages}
                onPageChange={this.handlePaginationChange}
            />
        </span>;
    }
}