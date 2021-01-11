// ^ 起始位置， $ 结尾位置
// \\b = \b  单词边界
// name = csrf_token
// (): 提取参数的内容
// []: 所有的可能性
// [^;]: ^取反+; = 除了分号全部的字符串

function getCookie(name){
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined ;
}
