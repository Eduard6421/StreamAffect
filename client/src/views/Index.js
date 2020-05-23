import React from "react";

// reactstrap components

// core components
import Navbar from "components/Navbar.js";
import Header from "components/Header.js";

// index sections

function Index() {
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
      <Header />
      <div className="main">
      </div>
    </>
  );
}

export default Index;
