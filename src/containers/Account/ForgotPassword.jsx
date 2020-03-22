import React, { Component } from "react";
import { Container, Row, Col } from "react-bootstrap";

import ForgotPasswordForm from "../../components/Form/ForgotPasswordForm";
import "./Accounts.scss";

import Logo from "./../../assets/img/logo.png";
export default class Login extends Component {
  render() {
    return (
      <div className="account-page">
        <Container className="d-flex flex-column justify-content-center align-items-center">
          <div className="logo pb-5">
            <img src={Logo} class="logo" alt="logo raven raffles"></img>
          </div>

          <ForgotPasswordForm></ForgotPasswordForm>
        </Container>
      </div>
    );
  }
}
