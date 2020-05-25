import { handleResponse } from "helpers/handle-response.js";

// port Edi
const apiUrl = "http://84.117.81.51:5000";

export const predictionsService = {
  upload,
  getAll,
};

function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
  return time;
}

function upload() {
  const requestOptions = {
    method: "POST",
  };

  return fetch(`${apiUrl}/upload`, requestOptions)
    .then(handleResponse)
    .then((data) => {
      return data;
    });
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
