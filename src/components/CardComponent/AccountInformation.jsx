import React, { Component } from "react";
import "./CardComponent.scss";

const CardComponent = props => {
  return (
    <div
      class="card-gradient mt-3 pb-1 mt-md-0 d-flex flex-column"
      id="account-info"
    >
      <div class="info">
        <a class="text-bold text-white mb-1">Account Information</a>
      </div>

      <div className="row">
        <div className="col-md-6">
          <div class="profiles-info d-flex justify-content-between">
            <a class="profile-label">Profiles</a>
            <a class="text-white">
              {props.profiles} <i class="fas fa-check ml-2"></i>
            </a>
          </div>
          <div class="profiles-info d-flex justify-content-between">
            <a class="profile-label">Proxies</a>
            <a class="text-white">
              {props.proxies} <i class="fas fa-check ml-2"></i>
            </a>
          </div>
        </div>
        <div className="col-md-6">
          <div class="profiles-info d-flex justify-content-between">
            <a class="profile-label">Anti Captcha Balance</a>
            <a class="text-white">
              {props.balance} <i class="fas fa-check ml-2"></i>
            </a>
          </div>
          <div class="profiles-info d-flex justify-content-between">
            <a class="profile-label">Status</a>
            <a class="text-white">
              {props.status} <i class="fas fa-check ml-2"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardComponent;
