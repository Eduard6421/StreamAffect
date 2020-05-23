/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container, Row, Col } from "reactstrap";

// core components
import ImageUpload from "components/ImageUpload.js";

function IndexHeader() {
  return (
    <>
      <div
        className="page-header section-dark"
        style={{
          backgroundImage:
            "url(" + require("assets/img/antoine-barres.jpg") + ")",
        }}
      >
        <div className="filter" />
        <div className="content-center" >
          <Container>
            <div className="title-brand">
              {/* <h1 className="presentation-title">Paper Kit React</h1> */}
            </div>
            <h2 className="presentation-subtitle text-center">
              Upload one image and let us guess your emotion!
            </h2>
            <br />
            <br />
            <Row>
              <Col md="3" sm="2"></Col>
              <Col md="6" sm="8">
                <ImageUpload />
              </Col>
              <Col md="3" sm="2"></Col>
            </Row>
          </Container>
        </div>
        <div
          className="moving-clouds"
          style={{
            backgroundImage: "url(" + require("assets/img/clouds.png") + ")",
          }}
        />
      </div>
    </>
  );
}

export default IndexHeader;
