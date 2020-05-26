import { handleResponse } from "helpers/handle-response.js";

// port Edi
const apiUrl = "http://84.117.81.51:5000";

export const predictionsService = {
  upload,
  getAll,
  getAllIds,
  getImage,
};

function upload(image) {
  console.log(image);

  // const requestOptions = {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "image/jpeg"
  //   },
  //   body: image,
  // };

  // return fetch(`${apiUrl}/upload`, requestOptions)
  //   .then((response) => {
  //     return response;
  //   });

  var req = new XMLHttpRequest();

  req.open("POST", "http://84.117.81.51:5000/upload", true);
  req.send(image);
}

function getAllIds() {
  const requestOptions = {
    method: "GET",
  };

  return fetch(`${apiUrl}/get_ids?num_images=50`, requestOptions)
    .then(handleResponse)
    .then((data) => {
      data = data.sort(function (a, b) {
        return (
          parseInt(b.created_at.split(".")[0]) -
          parseInt(a.created_at.split(".")[0])
        );
      });

      return data;
    })
    .catch((e) => {
      console.log(e);
    });
}

function getAll() {
  const requestOptions = {
    method: "GET",
  };

  return fetch(`${apiUrl}/list?num_images=50`, requestOptions)
    .then(handleResponse)
    .then((data) => {
      data = data.sort(function (a, b) {
        return (
          parseInt(b.created_at.split(".")[0]) -
          parseInt(a.created_at.split(".")[0])
        );
      });

      return data;
    })
    .catch((e) => {
      console.log(e);
    });
}

function getImage(imageId) {
  const requestOptions = {
    method: "GET",
  };

  return fetch(`${apiUrl}/get_image?image_id=${imageId}`, requestOptions)
  .then(handleResponse)
  .then((data) => {
    return data;
  })
  .catch((e) => {
    console.log(e);
  });
}
