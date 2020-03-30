import React, { Component } from "react";
import "./CardComponent.scss";

import ArrowIcon from "../../assets/img/arrow-circle.png";

const CardComponent = props => {
  return (
    <div class="card-gradient d-flex">
      <div class="info">
        <a class="text-bold text-white">Raffle Submitted </a>
        <h1 class="text-semibold">{props.submitted}</h1>
      </div>
      <div class="card-image d-flex justify-content-end">
        <img src={ArrowIcon} class="check-icon align-self-center"></img>
      </div>
    </div>
  );
};

export default CardComponent;
