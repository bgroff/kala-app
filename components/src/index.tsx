import * as React from "react";
import * as ReactDOM from "react-dom";

import { UserForm } from "./components/UserForm";
import { Provider } from 'mobx-react'
import { stores } from "./stores/index";
import { Component } from "react";


export default class RootComponent extends Component {
    render() {
      return (
        <Provider {...stores}>
          <UserForm />
        </Provider>
      )
    }
  }

ReactDOM.render(
    <RootComponent/>,

    document.getElementById("document-permissions-form")
);
