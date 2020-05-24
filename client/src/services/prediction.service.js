import { handleResponse } from "helpers/handle-response.js";

const apiUrl = "http://localhost:4000";

export const predictionService = {
    predict
}

function predict() {
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