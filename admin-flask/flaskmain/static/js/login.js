$(document).ready(function(){
              var uuid = makeuuid();
              $('#uuid').attr('value', uuid);
              $("#codeClick").attr('src','/image_codes/'+uuid+'.png');
            });
$(document).ready(function(){
              $("#codeClick").click(function(){
                  // alert("点击了");
                  var uuid = makeuuid();
                  $('#uuid').attr('value', uuid);
                  $("#codeClick").attr('src','/image_codes/'+uuid+'.png');
              });
            });

function makeuuid() { // 看起来像，但实际上不是的，要注意这个
        var withLine = false; //带不带横线
        var len = 36; //长度为36
        var radix = 16; //16进制
        var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
        var uuid = [], i;
        radix = radix || chars.length;
        if (withLine) {
            var r;
            uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
            uuid[14] = '4';
            for (i = 0; i < len; i++) {
                if (!uuid[i]) {
                    r = 0 | Math.random() * 16;
                    uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r];
                }
            }
        } else {
            for (i = 0; i < len; i++) {
                uuid[i] = chars[0 | Math.random() * radix];
            }
        }
        return uuid.join('');
    }
