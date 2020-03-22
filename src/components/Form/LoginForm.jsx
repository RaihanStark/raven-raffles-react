import React from "react";
import "./Form.scss";

import { Link } from "react-router-dom";
import { Button, Spinner } from "react-bootstrap";

const LoginForm = () => {
  return (
    <div className="login-form d-flex flex-column align-items-center">
      <p id="app-text" class="mt-3">
        Login To Your Account
      </p>
      <input class="form-input" placeholder="Username" type="text" />
      <input
        class="form-input"
        placeholder="Password"
        type="password"
        name=""
        id=""
      />
      <Button className="form-submit text-bold">Login</Button>
      {/* <input class="form-submit text-bold" type="submit" value="Login" /> */}

      <Link to="/register" className="text-white mt-3">
        Don't have an account? <span class="text-bold">Sign Up</span>
      </Link>

      <Link to="/forgot-password" className="text-white text-bold mb-3">
        Forgot Password
      </Link>
    </div>
  );
};

export default LoginForm;
