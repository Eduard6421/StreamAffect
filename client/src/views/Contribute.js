import React from "react";

// reactstrap components

// core components
import Navbar from "components/Navbar.js";
import ContributeHeader from "components/ContributeHeader.js";

// index sections

function Contribute() {
  document.documentElement.classList.remove("nav-open");
  React.useEffect(() => {
    document.body.classList.add("index");
    return function cleanup() {
      document.body.classList.remove("index");
    };
  });
  return (
    <>
      <Navbar />
      <ContributeHeader />
      <div className="main">
      </div>
    </>
  );
}

export default Contribute;
