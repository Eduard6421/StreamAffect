import React from "react";

// reactstrap components

// core components
import Navbar from "components/Navbar.js";
import HomeHeader from "components/HomeHeader.js";

// index sections

function Home() {
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
      <HomeHeader />
      <div className="main">
      </div>
    </>
  );
}

export default Home;
