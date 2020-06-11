import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Redirect, Switch } from "react-router-dom";

// styles
import "assets/css/bootstrap.min.css";
import "assets/scss/paper-kit.scss";
import "assets/demo/demo.css";
// pages
import Home from "views/Home.js";
import Contribute from "views/Contribute.js"
// others

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      {/* <Route path="/contribute" render={props => <Contribute {...props} />} /> */}
      <Route path="/predict" render={props => <Home {...props} />} />
      <Redirect to="/predict" />
    </Switch>
  </BrowserRouter>,
  document.getElementById("root")
);
