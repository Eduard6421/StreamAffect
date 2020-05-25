import React from "react";

// reactstrap components

// core components
import Navbar from "components/Navbar.js";
import HomeHeader from "components/HomeHeader.js";
import PredictionsList from "components/PredictionsList.js";

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
      <PredictionsList />
      <div className="main">
      </div>
    </>
  );
}

export default Home;
