import { handleResponse } from "helpers/handle-response.js";

// port Edi
const apiUrl = "http://84.117.81.51:5000";

export const predictionService = {
    upload
}

function upload() {
    const requestOptions = {
        method: "POST",
        // headers: ""
      }

      return fetch(`${apiUrl}/upload`, requestOptions)
      .then(handleResponse)
      .then((response) => {
        return response;
      });
}