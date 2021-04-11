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

//  判断是否有特殊字符
function RegeMatch(){
    var pattern = new RegExp("[~'!@#$%^&*()-+_=:]");
    if($("#name").val() != "" && $("#name").val() != null){
        if(pattern.test($("#name").val())){
            alert("非法字符！");
            $("#name").attr("value","");
            $("#name").focus();
            return false;
        }
    }
}

// 判断是否符合某个正则表达式
// testd_string： 测试字符
// pattern ： 正则表达式  var pattern = new RegExp("[~'!@#$%^&*()-+_=:]");
// var startTimeForm = /^[0-9]{4}-[0-1]?[0-9]{1}-[0-3]?[0-9]{1} 00:00:00$/;
// return ： true 为不符合; false 为符合
function is_correct_re(testd_string, pattern){
    if(testd_string == "" || testd_string == null){
        return true;
    }else if(!pattern.test(testd_string)){
        return true;
    }else{
        return false;
    }
}

function is_correct_string(testd_string, pattern){
    if(testd_string == "" || testd_string == null){
        return true;
    }else if(pattern.test(testd_string)){
        return true;
    }else{
        return false;
    }
}
