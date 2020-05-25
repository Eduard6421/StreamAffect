import { handleResponse } from "helpers/handle-response.js";

// port Edi
const apiUrl = "http://84.117.81.51:5000";

export const predictionsService = {
  upload,
  getAll,
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

function getAll() {
  const requestOptions = {
    method: "GET",
  };

  return fetch(`${apiUrl}/list`, requestOptions)
    .then((handleResponse))
    .then((data) => {
      
      data = data.sort(function(a, b) {
        return parseInt(b.created_at.split(".")[0]) - parseInt(a.created_at.split(".")[0]) ;
      })

      return data;
    }).catch(e => {
      console.log(e);
  });
}
