import React, { Component } from "react";
import "./Dashboard.scss";

import Navbar from "../../components/NavbarComponent/NavbarComponent";

import RaffleAvailable from "../../components/CardComponent/RaffleAvailable";
import RaffleSubmitted from "../../components/CardComponent/RaffleSubmitted";
import AccountInformation from "../../components/CardComponent/AccountInformation";
export default class Dashboard extends Component {
  render() {
    return (
      <div className="dashboard">
        <div className="container">
          <Navbar />

          <div className="row mt-3 mt-md-5">
            <div className="col-md-3">
              <RaffleAvailable available="2"></RaffleAvailable>
            </div>
            <div className="col-md-3 mt-3 mt-md-0">
              <RaffleSubmitted submitted="3"></RaffleSubmitted>
            </div>
            <div className="col-md-6">
              <AccountInformation
                profiles="Profile 4"
                proxies="US Residental"
                balance="$24"
                status="Activated"
              ></AccountInformation>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
