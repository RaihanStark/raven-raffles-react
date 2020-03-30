import React, { Component } from "react";
import "./Form.scss";

import { Link } from "react-router-dom";
import { Button, Spinner } from "react-bootstrap";

import Swal from "sweetalert2";
import axios from "../../client";

export default class LoginForm extends Component {
  doLogin = e => {
    e.preventDefault();

    axios
      .post("/login", {
        username: this.refs.username.value,
        password: this.refs.password.value
      })
      .then(res => {
        Swal.fire(
          "Login Success",
          "You will redirect in 3 seconds.",
          "success"
        );
      })
      .catch(err => {
        Swal.fire("Error", err.response.data.msg, "error");
      });
  };
  render() {
    return (
      <div className="login-form d-flex flex-column align-items-center">
        <p id="app-text" class="mt-3">
          Login To Your Account
        </p>
        <form
          className="d-flex flex-column align-items-center"
          onSubmit={this.doLogin}
        >
          <input
            class="form-input"
            placeholder="Username"
            type="text"
            ref="username"
          />
          <input
            class="form-input"
            placeholder="Password"
            type="password"
            ref="password"
          />
          <input class="form-submit text-bold" type="submit" value="Sign In" />
        </form>

        <Link to="/register" className="text-white mt-3">
          Don't have an account? <span class="text-bold">Sign Up</span>
        </Link>

        <Link to="/forgot-password" className="text-white text-bold mb-3">
          Forgot Password
        </Link>
      </div>
    );
  }
}
