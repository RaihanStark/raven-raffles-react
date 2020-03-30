import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import "./App.css";
import Login from "../Account/Login";
import Register from "../Account/Register";
import ForgotPassword from "../Account/ForgotPassword";
import Dashboard from "../Dashboard/Dashboard";

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/login">
          <Login />
        </Route>
        <Route path="/register">
          <Register />
        </Route>
        <Route path="/forgot-password">
          <ForgotPassword />
        </Route>
        <Route path="/dashboard">
          <Dashboard />
        </Route>
      </Switch>
      {/* <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
          </ul>
        </nav> */}
    </Router>
  );
}

export default App;
