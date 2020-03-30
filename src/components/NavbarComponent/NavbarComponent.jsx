import React from "react";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import "./NavbarComponent.scss";
import Logo from "../../assets/img/logo.png";

export default function NavbarComponent() {
  return (
    <Navbar expand="lg">
      <img src={Logo} class="navbar-logo" alt=""></img>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item active">
            <a class="nav-link text-white mx-1" href="/dashboard.html">
              Dashboard
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white mx-1" href="/dashboard.html">
              Tasks
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white mx-1" href="/dashboard.html">
              Accounts
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white mx-1" href="/dashboard.html">
              Proxies
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white mx-1" href="/dashboard.html">
              Profiles
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white mx-1" href="/dashboard.html">
              Settings
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white mx-1" href="/dashboard.html">
              Documentation
            </a>
          </li>
        </ul>
      </div>
    </Navbar>
  );
}
