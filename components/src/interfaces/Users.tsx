export interface UserProps { name: string, id: number, can_create: string, can_invite: string, can_manage: string }
export interface UsersProps extends Array<UserProps> { }
export interface UsersList { users: UsersProps }
export interface UserState { can_create: string, can_invite: string, can_manage: string }
export interface FormState { csrf_token: string }
