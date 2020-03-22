import React from "react";
import "./Form.scss";

import { Link } from "react-router-dom";

const RegisterForm = () => {
  return (
    <div className="login-form d-flex flex-column align-items-center">
      <p id="app-text" class="mt-3">
        Register Account
      </p>
      <input class="form-input" placeholder="License Key" type="text" />
      <input class="form-input" placeholder="Email" type="email" />
      <input class="form-input" placeholder="Username" type="text" />
      <input
        class="form-input"
        placeholder="Password"
        type="password"
        name=""
        id=""
      />
      <input class="form-submit text-bold" type="submit" value="Sign Up" />
      <Link to="/login" className="text-white mt-3">
        Do you have an account? <span class="text-bold">Sign In</span>
      </Link>
      <Link to="/forgot-password" className="text-white text-bold mb-3">
        Forgot Password
      </Link>
    </div>
  );
};

export default RegisterForm;
