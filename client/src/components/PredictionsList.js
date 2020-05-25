import React from "react";

// reactstrap components
import {
  Container,
  Row,
  Col,
  Button,
  Card,
  CardBody,
  CardFooter,
  CardImg,
  CardImgOverlay,
  CardLink,
  CardTitle,
  CardSubtitle,
  CardText,
  ListGroupItem,
  ListGroup,
} from "reactstrap";

// core components

import { predictionsService } from "services/predictions.service";

class PredictionsList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isFetching: false,
      data: [],
    };
  }

  componentDidMount() {
    this.getAllPredictions();
  }

  getAllPredictions() {
    this.setState({ isFetching: true });

    predictionsService.getAll().then((data) => {
      console.log(data);

      this.setState({ data: data });
    });

    this.setState({ isFetching: false });
  }

  render() {
    return (
      <>
        <div className="section section-dark section-summary">
          <Container>
            <Col className="ml-auto mr-auto" md="8">
              <div className="section-description text-center">
                <h2 className="title">Latest Predictions</h2>

                <h4>
                  <b>
                    {this.state.isFetching ? "Fetching predictions..." : ""}
                  </b>
                </h4>
              </div>
            </Col>
          </Container>
          <Container className="ml-auto mr-auto">
            <Row>
              {this.state.isFetching
                ? ""
                : this.state.data.map(function (item, i) {
                    console.log(item);

                    var imageSrc = "data:image/jpeg;base64," + item.image;

                    return (
                      <Col className="ml-auto mr-auto" md="4" sm="8">
                        <Card className="card-image card-hover-effect">
                          <CardImg alt="..." src={imageSrc} top></CardImg>
                          <CardBody className="text-center">
                            <CardTitle tag="h5">
                              <b>
                                {(() => {
                                  if (item.predictions_lr.anger == 1) {
                                    return <p>ANGER</p>;
                                  } else if (item.predictions_lr.fear == 1) {
                                    return <p>ANGER</p>;
                                  } else if (item.predictions_lr.happy == 1) {
                                    return <p>HAPPY</p>;
                                  } else if (item.predictions_lr.horny == 1) {
                                    return <p>EXCITED</p>;
                                  } else if (item.predictions_lr.sad == 1) {
                                      return <p>SAD</p>
                                  }
                                })()}
                                <br />
                                <img
                                  src={require("assets/icons/happiness.svg")}
                                  width="35px"
                                />{" "}
                                - {item.predictions_nn.happy.toFixed(3)}
                                <br />
                                <img
                                  src={require("assets/icons/excited.svg")}
                                  width="35px"
                                />{" "}
                                - {item.predictions_nn.horny.toFixed(3)}
                                <br />
                                <img
                                  src={require("assets/icons/sad.svg")}
                                  width="35px"
                                />{" "}
                                - {item.predictions_nn.sad.toFixed(3)}
                                <br />
                                <img
                                  src={require("assets/icons/scared.svg")}
                                  width="35px"
                                />{" "}
                                - {item.predictions_nn.fear.toFixed(3)}
                                <br />
                                <img
                                  src={require("assets/icons/angry.svg")}
                                  width="35px"
                                />{" "}
                                - {item.predictions_nn.anger.toFixed(3)}
                              </b>
                            </CardTitle>
                          </CardBody>
                        </Card>
                      </Col>
                    );
                  })}
            </Row>
          </Container>
        </div>
      </>
    );
  }
}

export default PredictionsList;
