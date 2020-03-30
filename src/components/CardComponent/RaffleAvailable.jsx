import React, { Component } from "react";
import "./CardComponent.scss";

import CheckIcon from "../../assets/img/check-circle.png";

const CardComponent = props => {
  return (
    <div class="card-gradient d-flex">
      <div class="info">
        <a class="text-bold text-white">Raffles Available </a>
        <h1 class="text-semibold">{props.available}</h1>
      </div>
      <div class="card-image d-flex justify-content-end">
        <img src={CheckIcon} class="check-icon align-self-center"></img>
      </div>
    </div>
  );
};

export default CardComponent;
