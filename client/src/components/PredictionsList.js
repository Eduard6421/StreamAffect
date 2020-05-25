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
                <h2 className="title">All Predictions</h2>

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
                          <CardImg
                            alt="..."
                            src={imageSrc}
                            top
                          ></CardImg>
                          <CardBody>
                            <CardText>
                            <i class="fa fa-frown-o"></i>
                            </CardText>
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
