<template>
<div id="Register">
       
    
        <div style="margin-top:3rem">
            <el-row :gutter="10" >
                <el-col class="form" :xs="24" :sm="{span: 12, offset: 6}" :md="{span: 20, offset: 2}" :lg="{span: 8, offset: 8}" :xl="{span: 6, offset: 9}">
                    <h1>嗨商城注册页面</h1>

                    uuidNumber: {{ uuidNumber }}
                </el-col>
            </el-row> 
        
            <el-row :gutter="10"  >
                <el-col class="form" :xs="24" :sm="{span: 12, offset: 6}" :md="{span: 20, offset: 2}" :lg="{span: 8, offset: 8}" :xl="{span: 8, offset: 8}" >
                    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="el-form el-form--label-left demo-ruleForm"  label-width="80px" >
                        
                        <el-form-item prop="phoneNumber"  label="手机号码">
                            <el-input id="phoneNumber" type="text" v-model="ruleForm.phoneNumber"  prefix-icon="el-icon-phone" placeholder="输入中国境内电话"></el-input>
                            
                        </el-form-item>
                        
                        <el-form-item prop="imageCode" label="图片验证">
                            <el-input id="imageCode" type="text" v-model="ruleForm.imageCode" prefix-icon="el-icon-picture" placeholder="验证码不区分大小写" style="width:60%;;float: left;display: inline-block;" ></el-input>
                            <img :src="'http://127.0.0.1:5000/api/v1.0/image_codes/'+uuidNumber" v-on:click="ImgChange" alt="" style="max-width:35%;height:40px;float: left;display: inline-block;margin-left:5%;text-align:center" >
                        </el-form-item>
                        
                        <el-form-item prop="phoneCode" label="短信验证">
                            <el-input id="phoneCode" type="text" v-model="ruleForm.phoneCode"  prefix-icon="el-icon-message" placeholder="短信验证码" style="width:60%" ></el-input>
                            <el-button type="success" @click="getSMSCode(is_match.is_image_match)" style="width:40%" :disabled="is_match.is_image_match">短信验证码</el-button>
                        </el-form-item>
                        
                        <el-form-item prop="password" label="密码">
                            <el-input id="password" type="text" v-model="ruleForm.password"  prefix-icon="el-icon-loading" placeholder="输入密码" ></el-input>
                        </el-form-item>
                        
                        <el-form-item prop="repeatPassword" label="重复密码">
                            <el-input id="repeatPassword" type="text" v-model="ruleForm.repeatPassword"  prefix-icon="el-icon-loading" placeholder="两次输入密码必须一致" ></el-input>
                        </el-form-item>
                        <!-- <el-button type="primary" @click="submitForm('ruleForm2')">提交</el-button>
                        <el-button @click="resetForm('ruleForm2')">重置</el-button> -->
                        <el-form-item>
                            <el-button  style="width:45%;float:left;margin-top:2rem" @click="emptyForm">重置</el-button>
                            <el-button type="primary" style="width:45%;float:right;margin-top:2rem" @click="submitForm('ruleForm')" :disabled="buttonStatus.registerStatus">马上注册</el-button>
                        </el-form-item>
                    </el-form>
                    <div style="width:55%;float:right;margin-top:3rem;font-size:18px">已经有帐号？<a href="/#/login" style="color:#E6A23C">点击登录</a></div>
                </el-col>
                
            </el-row>
        </div>
 


    
</div>    
</template>



<script>
import { reactive, ref, onMounted, onBeforeUnmount  } from "@vue/composition-api";
import uuid from "uuid";
import { GetCates, GetCodeImg } from "../apis/read.js";
import { Register } from "../apis/users/register.js";
import { getInofs, postInofs } from "../apis/fournight.js";


export default {
    name: "Register",
    components:{},

    setup(props, context){
        // beforeCreate -> 请使用 setup()
        // created -> 请使用 setup()
        // beforeMount -> onBeforeMount
        // mounted -> onMounted
        // beforeUpdate -> onBeforeUpdate
        // updated -> onUpdated
        // beforeDestroy -> onBeforeUnmount
        // destroyed -> onUnmounted
        // errorCaptured -> onErrorCaptured
        const getImgParams = reactive({
            url: ''
        });

        GetCates(getImgParams).then((resp)=>{
            console.log("register : resp.data = ",resp.data)
        });   

        

        onMounted(()=>{
            document.querySelector('body').setAttribute('style', 'background:url("/images/register_background.jpg") no-repeat; background-position: center;background-attachment:fixed');
        });
        // 背景颜色	{background-color:数值}
        // 背景图片	{background-image: url(URL)|none}
        // 背景重复	{background-repeat:inherit|no-repeat|repeat|repeat-x|repeat-y}
        // 背景固定	{background-attachment:fixed|scroll}
        // 背景定位	{background-position:数值|top|bottom|left|right|center}
        // 背影样式	{background:背景颜色|背景图象|背景重复|背景附件|背景位置}


        onBeforeUnmount(()=>{
            document.querySelector('body').removeAttribute('style');
        });

        

        const uuidNumber = ref(uuid.v4());

        const ImgChange = ()=>{
            uuidNumber.value = uuid.v4();
        };

        const buttonStatus = reactive({
            smsStatus: true,
            registerStatus: true
        });
        const is_match = reactive({
                is_image_match: true,
                is_sms_match: true
            }); 

        const imageCodeFromBack = reactive({
            value: ''
        });
        const getImageParams = reactive({
                url: "/image_codes_values/"+ uuidNumber.value,
                data:''
            });
        getInofs(getImageParams).then((resp)=>{
            // is_match.is_image_match = true;
            imageCodeFromBack.value = resp.data.data.image_numbers
        }).catch(error =>{
            context.root.$message({
                message: "验证码已经失效，请刷新后重新输入",
                type: 'Danger'
            });
        });
        
        const checkImageCode = (value) => {
            // is_match.is_image_match = true;
            console.log("imageCodeFromBack.value =&&&&&&&&&&&&&&&&&&&&&&", imageCodeFromBack.value)
            console.log("value =&&&&&&&&&&&&&&&&&&&&&&", value)
            getImageParams.url = "/image_codes_values/"+ uuidNumber.value;
            getInofs(getImageParams).then((resp)=>{
                // is_match.is_image_match = true;
                imageCodeFromBack.value = resp.data.data.image_numbers
            }).catch(error =>{
                context.root.$message({
                    message: "验证码已经失效，请刷新后重新输入",
                    type: 'Danger'
                });
            });
            if(imageCodeFromBack.value.toLowerCase() == value.toLowerCase()){
                is_match.is_image_match =  false;
            } else{
                context.root.$message({
                    message: "验证码错误",
                    type: 'Danger'
                });
                is_match.is_image_match =  true;
            }

        }
      
        

        // 表单验证方法
        const validatePhoneNumber = (rule, value, callback) =>{
            buttonStatus.smsStatus = true;
            buttonStatus.registerStatus = true;
            // let reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            let reg = /^1[3456789]\d{9}$/;
            if (value === '') {
                callback(new Error('用户名为电话号码，且不能为空'));
            } else if(!reg.test(value)){
                callback(new Error('电话号码格式有误'));
            } else {
                callback();
            }
        };
        
        const validateImageCode = (rule, value, callback) =>{
            buttonStatus.smsStatus = true;
            buttonStatus.registerStatus = true;
            // is_match.is_image_match = true;
            
            let numReg = /^[A-Za-z0-9]{6}$/; 
            // let numReg = /[A-Za-z].*[0-9]|[0-9].*[A-Za-z]/;
            if (!value) {
                buttonStatus.smsStatus = true;
                callback(new Error('验证码不能为空'));
            } else if(!numReg.test(value)){
                buttonStatus.smsStatus = true;
                callback(new Error('验证码为6位的数字和字母(区分大小写)'))
            } else{
                buttonStatus.smsStatus = false;
                buttonStatus.registerStatus = false;
                callback();
            }
            checkImageCode(value);
        };
        const validatePhoneCode = (rule, value, callback) =>{
            buttonStatus.smsStatus = false;
            buttonStatus.registerStatus = true;
            let reg = /^[0-9]{6}$/;
            if(!value){
                callback(new Error('手机验证码不能为空'));
            } else if(!reg.test(value)){
                callback(new Error('手机验证码为6位的数字'));
            } else{
                buttonStatus.smsStatus = false;
                buttonStatus.registerStatus = false;
                callback();
            }
        };
        const validatePassword = (rule, value, callback) => {
            buttonStatus.smsStatus = false;
            buttonStatus.registerStatus = true;
            let passwordreg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$/;
            if (value === '') {
                callback(new Error('密码不能为空'));
            }else if(!passwordreg.test(value)){
                callback(new Error('密码必须：字母、数字; 长度在6到20位之间'))
            } else {
                callback();
            }
            
        };
        const validateRepeatPassword = (rule, value, callback) =>{
            buttonStatus.smsStatus = false;
            buttonStatus.registerStatus = true;
            if (value === '') {
                callback(new Error('密码不能为空'));
            }else if(value != ruleForm.password){
                callback(new Error('两次输入密码不一致'))
            } else {
                buttonStatus.smsStatus = false;
                buttonStatus.registerStatus = false;
                callback();
            }
        };
        const emptyForm = ()=>{
            ruleForm.phoneNumber='';
            ruleForm.imageCode='';
            ruleForm.phoneCode='';
            ruleForm.password='';
            ruleForm.repeatPassword='';
            buttonStatus.smsStatus = true;
            buttonStatus.registerStatus = true;
        };

        const getSMSCode = (value) =>{
            // is_match.is_image_match = true;
            if(ruleForm.phoneNumber == ''){
                context.root.$message.error('电话不能为空，不然验证码不知道往哪里发');
                return false
            }
            

            if(value){
                console.log("ruleForm.imageCode ====", ruleForm.imageCode)
                context.root.$message({
                        message: "图片验证码错误，请确认后重新输入",
                        type: 'Danger'
                    });
            } else{
                // 开始发送请求
                const paramsSMS = reactive({
                    url:'/send_sms_codes/'+ ruleForm.phoneNumber+'?image_uuid='+uuidNumber.value+'&image_code='+ruleForm.imageCode,
                    data: ''
                });

                getInofs(paramsSMS).then((resp)=>{
                    console.log("手机验证码向服务器的请求结果====", resp);
                    context.root.$message({
                        message: "验证码已发送到您的手机，请注意查收",
                        type: 'Danger'
                    });
                }).catch((error)=>{
                    console.log("手机验证码向服务器的请求结果==错误==", error);
                    context.root.$message({
                        message: error.message,
                        type: 'Danger'
                    });
                })
                
            }

        };

        const submitForm = (formName =>{
            context.refs[formName].validate((valid) => {
            // 这个地方的contex表现了，context内大概率就是保存着来自当前页面的信息
            if (valid) {
                alert('submit!');
                const registerData = reactive({
                    url:"/users/register",
                    data:{
                        phoneNumber: ruleForm.phoneNumber,
                        password: ruleForm.password,
                        repeatPassword: ruleForm.repeatPassword,
                        phoneCode: ruleForm.phoneCode,
                        // csrf_token: 
                    }
                });
                console.log(registerData)
                // Register(registerData).then(response => {}).catch(error =>{})
                postInofs(registerData).then((resp) =>{
                    console.log(resp)
                }).catch((e) => {
                   context.root.$message({
                    message: e.message,
                    type: 'Danger'
                }); 
                })
                
            } else {
                console.log('error submit!!');
                return false;
            }
            })
        });

        // 表单内容
        const ruleForm = reactive({  // 更多得想预先设计好了一个容器，去接纳来自当前页面的数据
            phoneNumber: '',
            imageCode: '',
            phoneCode: '',
            password: '',
            repeatPassword: ''
        });
        // 表单验证方法和触发条件
        const rules = reactive({
            phoneNumber: [
                { validator: validatePhoneNumber, trigger: 'blur' } // tirgger 触发规则， blur： 失去焦点的时候触发
            ],
            imageCode: [
                { validator: validateImageCode, trigger: 'blur' } // tirgger 触发规则， blur： 失去焦点的时候触发
            ],
            phoneCode: [
                { validator: validatePhoneCode, trigger: 'blur' } // tirgger 触发规则， blur： 失去焦点的时候触发
            ],
            password: [
                { validator: validatePassword, trigger: 'blur' } // tirgger 触发规则， blur： 失去焦点的时候触发
            ],
            repeatPassword: [
                { validator: validateRepeatPassword, trigger: 'blur' } // tirgger 触发规则， blur： 失去焦点的时候触发
            ],
        });

        // renturn中为所有要在template中用到的数据和方法
        return {
            // 下面是基础数据类型，就是用ref定义的
            uuidNumber,
            // 下面的是对象数据类，就是reactive定义的
            ruleForm,
            rules,
            buttonStatus,
            is_match,
            // 下面的方法
            ImgChange,

            validatePhoneNumber,
            validateImageCode,
            validatePhoneCode,
            validatePassword,
            validateRepeatPassword,
            emptyForm,
            getSMSCode,
            submitForm
        }
    }


}
</script>


<style lang="scss" scoped>
    // .register_background {
    //     // background: url(/register_background.jpg) no-repeat ;
    //     background-image: url(../assets/register_background.jpg);
    //     background-size: cover;
    //     font-size: 16px;
    // }
    .form{background: rgba(255,255,255,0.3);padding-bottom: 1rem;padding-left: 5rem;padding-right: 5rem;padding-bottom: 1rem;vertical-align: middle;}
    #login_form{display: block;}
    #register_form{display: none;}
    .fa{display: inline-block;top: 27px;left: 6px;position: relative;color: #ccc;}
    input[type="text"],input[type="password"]{padding-left:26px;}
    .checkbox{padding-left:21px;}
</style>