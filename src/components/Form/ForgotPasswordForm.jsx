import React from "react";
import "./Form.scss";

import { Link } from "react-router-dom";

const ForgotPasswordForm = () => {
  return (
    <div className="login-form d-flex flex-column align-items-center">
      <p id="app-text" class="mt-3">
        Forgot Password
      </p>
      <input class="form-input" placeholder="Email" type="email" />
      <input class="form-submit text-bold" type="submit" value="Send" />

      <Link to="/register" className="text-white mt-3">
        Don't have an account? <span class="text-bold">Sign Up</span>
      </Link>

      <Link to="/login" className="text-white mb-3">
        Do you have an account? <span class="text-bold">Sign In</span>
      </Link>
    </div>
  );
};

export default ForgotPasswordForm;
