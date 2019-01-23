import * as React from "react";
import * as ReactDOM from "react-dom";

import { UserForm} from "./components/UserForm";
import {UsersProps} from "./interfaces/Users";

declare var users: UsersProps;

ReactDOM.render(
    <UserForm users={users}/>,

    document.getElementById("user-form")
);
