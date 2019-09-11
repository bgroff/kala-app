import * as React from "react";
import * as ReactDOM from "react-dom";

import { DocumentUserForm } from "./components/DocumentUserForm";
import { ProjectUserForm } from "./components/ProjectUserForm";

import { Provider } from 'mobx-react'
import { stores } from "./stores/index";
import { Component } from "react";
import { OrganizationUserForm } from "./components/OrganizationUserForm";


export class DocumentRootComponent extends Component {
  render() {
    return (
      <Provider {...stores}>
        <DocumentUserForm />
      </Provider>
    )
  }
}

export class ProjectRootComponent extends Component {
  render() {
    return (
      <Provider {...stores}>
        <ProjectUserForm />
      </Provider>
    )
  }
}

export class OrganizationRootComponent extends Component {
  render() {
    return (
      <Provider {...stores}>
        <OrganizationUserForm />
      </Provider>
    )
  }
}

if (document.getElementById("document-permissions-form")) {
  ReactDOM.render(
    <DocumentRootComponent />,

    document.getElementById("document-permissions-form")
  );
}
if (document.getElementById("project-permissions-form")) {
  ReactDOM.render(
    <ProjectRootComponent />,

    document.getElementById("project-permissions-form")
  );
}
if (document.getElementById("organization-permissions-form")) {
  ReactDOM.render(
    <OrganizationRootComponent />,

    document.getElementById("organization-permissions-form")
  );
}
