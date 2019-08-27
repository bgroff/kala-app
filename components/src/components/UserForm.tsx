import * as React from "react";
import { UserFormUI } from "./UserFormUI";
import { Dropdown, Input, Pagination } from 'semantic-ui-react'
import { inject, observer } from "mobx-react";
import { IPermissionStore } from "../stores/PermissionStore";
import { DocumentPermissionStore } from "../stores/DocumentPermissionStore";


export enum PermissionTypes {
    None = "none",
    Create = "canCreate",
    Invite = "canInvite",
    Manage = "canManage",
}

export interface User {
    id: number,
    username: string,
    firstName: string,
    lastName: string
}

export interface Permission {
    id: number,
    canCreate?: boolean,
    canInvite?: boolean,
    canManage?: boolean,
    none?: boolean // really only here to keep the compiler happy.
}

export interface UserPermission {
    user: User,
    document?: Permission,
    project?: Permission,
    organization?: Permission

    onPermissionChange(id: number, newPermission: PermissionTypes, oldPermission: PermissionTypes): void; // Switch to enum
}

interface UserFormProps {
    permissionStore?: IPermissionStore
    documentPermissionStore?: DocumentPermissionStore

}

export interface UserFilterDropdown {
    onFilterChange: (event: any, data: any) => void
}

export interface UserNameFilter {
    onNameChange: (event: any, data: any) => void
}

export class UserNameFilterInput extends React.Component<UserNameFilter, {}> {
    render() {
        return <Input
            placeholder='Search'
            onChange={this.props.onNameChange}
        />
    }
}

const options = [
    { key: 0, text: "No filter", value: null },
    { key: 1, text: "No permissions", value: PermissionTypes.None },
    { key: 2, text: "Create permissions", value: PermissionTypes.Create },
    { key: 3, text: "Invite permissions", value: PermissionTypes.Invite },
    { key: 4, text: "Manage permissions", value: PermissionTypes.Manage },
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

export class UserForm extends React.Component<UserFormProps> {
    permissionStore: IPermissionStore;

    setUserPermissions = (id: number, newPermission: PermissionTypes, oldPermission: PermissionTypes) => {
        this.permissionStore.setPermission(id, newPermission, oldPermission);
    }

    onFilterChange = (event: any, data: any) => {
        this.permissionStore.setFilter(data.value);
    }

    onNameChange = (event: any, data: any) => {
        this.permissionStore.setSearch(data.value);
    }

    handlePaginationChange = (event: any, data: any) => {
        this.permissionStore.setActivePage(data.activePage);
    };

    render() {
        return <span>
            <div className="repo title">
                <div className="repo options">
                    <UserFilterDropdownMenu onFilterChange={this.onFilterChange} />
                </div>
                <UserNameFilterInput onNameChange={this.onNameChange} />
            </div>
            <div className="ui section divider"/>
            <Pagination
                activePage={this.permissionStore.activePage}
                totalPages={this.permissionStore.numberOfPages}
                onPageChange={this.handlePaginationChange}
            />
            <table className="ui very basic table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th></th>
                        <th>Manage acess</th>
                    </tr>
                </thead>
                <tbody>

                    {this.permissionStore.userPermissions.map((user, index) => <UserFormUI
                        key={index}
                        onPermissionChange={this.setUserPermissions}
                        {...user}
                         />)}
                </tbody>
            </table>
            <Pagination
                activePage={this.permissionStore.activePage}
                totalPages={this.permissionStore.numberOfPages}
                onPageChange={this.handlePaginationChange}
            />
        </span>;
    }
}