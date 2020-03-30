import React, { Component, setState } from "react";
import "./Form.scss";
import axios from "../../client";

import { Link } from "react-router-dom";

import Swal from "sweetalert2";
export default class RegisterForm extends Component {
  doRegister = e => {
    e.preventDefault();

    axios
      .post("/create_user", {
        username: this.refs.username.value,
        password: this.refs.password.value,
        licensekey: this.refs.key.value,
        email: this.refs.email.value
      })
      .then(res => {
        Swal.fire(
          "Registration Success",
          "Please Sign In to Your Account.",
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
          Register Account
        </p>
        <form
          onSubmit={this.doRegister}
          className="d-flex flex-column align-items-center"
        >
          <input
            class="form-input"
            placeholder="License Key"
            type="text"
            ref="key"
          />
          <input
            class="form-input"
            placeholder="Email"
            type="email"
            ref="email"
          />
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
          <input class="form-submit text-bold" type="submit" value="Sign Up" />
        </form>
        <Link to="/login" className="text-white mt-3">
          Do you have an account? <span class="text-bold">Sign In</span>
        </Link>
        <Link to="/forgot-password" className="text-white text-bold mb-3">
          Forgot Password
        </Link>
      </div>
    );
  }
}
