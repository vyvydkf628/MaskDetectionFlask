const request = require('request')
const url = "http://127.0.0.1:3010/mask"
const fs = require('fs')
const options = {
    method: "POST",
    url,
    headers: {
        "Content-Type": "multipart/form-data"
    },
    formData : {
        "image" : fs.createReadStream("./image/Aaron_Eckhart_0001.jpg")
    }
};

request(options, function (err, res, body) {
    if(err) console.log(err);
    console.log(body);
});
