import React from "react";
// used for making the prop types of this component
import PropTypes from "prop-types";

import { Button } from "reactstrap";

import defaultImage from "assets/img/image_placeholder.jpeg";
import defaultAvatar from "assets/img/image_placeholder.jpeg";

import { predictionsService } from "services/predictions.service";

function ImageUpload(props) {
  const [file, setFile] = React.useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = React.useState(
    props.avatar ? defaultAvatar : defaultImage
  );
  const fileInput = React.createRef();
  const handleImageChange = (e) => {
    e.preventDefault();
    let reader = new FileReader();
    let file = e.target.files[0];

    reader.onload = (evt) => {
      var req = new XMLHttpRequest();
      req.open("POST", "http://84.117.81.51:5000/upload", true);
      req.send(evt.target.result);

      let reader1 = new FileReader();
      reader1.readAsDataURL(file);
      reader1.onload = () => {
        setFile(reader1.result);
        setImagePreviewUrl(reader1.result);
      };

      //setFile(file);
      //setImagePreviewUrl(file);

      //document.getElementById("inputImage").remove();
    };

    reader.readAsArrayBuffer(file);
  };

  const handleClick = () => {
    fileInput.current.click();
  };

  const handleRemove = () => {
    setFile(null);
    setImagePreviewUrl(props.avatar ? defaultAvatar : defaultImage);
    fileInput.current.value = null;
  };
  return (
    <div className="fileinput text-center" id="inputImage">
      <input type="file" onChange={handleImageChange} ref={fileInput} />
      <div className={"thumbnail" + (props.avatar ? " img-circle" : "")}>
        <img src={imagePreviewUrl} alt="..." />
      </div>
      <div>
        {file === null ? (
          <Button
            className="btn-round"
            color="default"
            outline
            onClick={handleClick}
          >
            {props.avatar ? "Add Photo" : "Upload image"}
          </Button>
        ) : (
          <span>
            <div>
              <br />
              <h3>Done!</h3>
              <br />
            </div>
            <Button
              className="btn-round"
              outline
              color="default"
              onClick={handleClick}
            >
              Try again
            </Button>
            {props.avatar ? <br /> : null}
            {/* <Button
              color="danger"
              className="btn-round btn-link"
              onClick={handleRemove}
            >
              <i className="fa fa-times" />
              Try again
            </Button> */}
          </span>
        )}
      </div>
    </div>
  );
}

ImageUpload.propTypes = {
  avatar: PropTypes.bool,
};

export default ImageUpload;
