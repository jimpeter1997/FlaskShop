import service from "../utils/request.js";
// import { rsaEncrypt } from "../utils/rsa.js";

export  function getInofs(getParams){
    return service.request({
        method:"get",
        url: getParams.url,
        data: {
            jsdata: getParams.data,
            key:"" //rsaEncrypt(new Date().getTime()+':'+'alex'+':'+'otherinfos') // 预留字段给加密用
        }
    })
};

export function postInofs(postParams){
    return service.request({
        method:"post",
        url: postParams.url,
        data: {
            jsdata: postParams.data,
            key:"" //rsaEncrypt(new Date().getTime()+':'+'alex'+':'+'otherinfos') // 预留字段给加密用
        }
    })
}