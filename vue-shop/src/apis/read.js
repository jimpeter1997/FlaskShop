import service from "../utils/request.js";
// import { rsaEncrypt } from "../utils/rsa.js";


export function GetCodeImg(params){
    return service.request({
        method: "get",
        url:params.url,
        responseType:'stream'
    })
}

export function GetCates(getParams){
    return service.request({
        method: "get",
        url: getParams.url
    });
};

export function GetInfoPost(postParams){
    return service.request({
        method:'post',
        url:postParams.url,
        data:{
            key: postParams.key, // newest 
            secretKey: '' // rsaEncrypt(new Date().getTime()+':'+'alex'+':'+'otherinfos') // 预留字段给加密用
        }
    })
};

