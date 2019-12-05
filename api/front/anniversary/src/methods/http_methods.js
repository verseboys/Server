import axios from 'axios';

let post_form = function(url,data){
    return axios({
        url: url,
        method: 'post',
        data: data,
        transformRequest: [function (data) {
        // Do whatever you want to transform the data
          let ret = ''
          for (let it in data) {
            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
          }
          return ret
        }],
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
}

export default{
    post_form
}