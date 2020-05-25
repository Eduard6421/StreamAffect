/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container, Row, Col, Button } from "reactstrap";

// core components
import ImageUpload from "components/ImageUpload.js";

function ContributeHeader() {
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
        <div className="content-center">
          <Container>
            <div className="title-brand">
              {/* <h1 className="presentation-title">Paper Kit React</h1> */}
            </div>
            <h2 className="presentation-subtitle text-center">
              Help us improve the service by contributing with some data. Just upload some images!
            </h2>
            <br />
            <Row>
              <Col md="3" sm="2"></Col>
              <Col md="6" sm="8">
                <ImageUpload />
              </Col>
              <Col md="3" sm="2"></Col>
            </Row>
            <br />
            <Row>
              <Col md="3" sm="3"></Col>
              <Col md="6" sm="6">
                <Button className="btn-round" color="primary" type="button">
                  <i className="fa fa-heart"></i>
                  Contribute
                </Button>
              </Col>
              <Col md="3" sm="3"></Col>
            </Row>
            <br />
            <h5 className="presentation-subtitle text-center">
              You are not alone! Many thanks to all of you! More precisely: 6.234.737 contributors!
            </h5>
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

export default ContributeHeader;
