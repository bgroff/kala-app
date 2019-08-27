import * as React from "react";
import * as ReactDOM from "react-dom";

import { DocumentUserForm } from "./components/DocumentUserForm";
import { Provider } from 'mobx-react'
import { stores } from "./stores/index";
import { Component } from "react";


export default class RootComponent extends Component {
    render() {
      return (
        <Provider {...stores}>
          <DocumentUserForm />
        </Provider>
      )
    }
  }

// ReactDOM.render(
//     <RootComponent/>,

//     document.getElementById("user-form")
// );

ReactDOM.render(
  <RootComponent/>,

  document.getElementById("document-permissions-form")
);
