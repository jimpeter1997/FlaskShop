<template>
    <div id="Login">
        <div style="margin-top:3rem">
            <el-row :gutter="10" >
                <el-col class="form" :xs="24" :sm="{span: 12, offset: 6}" :md="{span: 20, offset: 2}" :lg="{span: 8, offset: 8}" :xl="{span: 6, offset: 9}">
                    <h1>嗨商城登录页面</h1>
                </el-col>
            </el-row> 
        
            <el-row :gutter="10"  >
                <el-col class="form" :xs="24" :sm="{span: 12, offset: 6}" :md="{span: 20, offset: 2}" :lg="{span: 8, offset: 8}" :xl="{span: 8, offset: 8}" >
                    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="el-form el-form--label-left demo-ruleForm"  label-width="80px" >
                        
                        <el-form-item prop="phoneNumber"  label="手机号码">
                            <el-input id="phoneNumber" type="text" v-model="ruleForm.phoneNumber"  prefix-icon="el-icon-phone" placeholder="输入中国境内电话"></el-input>
                            
                        </el-form-item>
                        
                        
                        
                        <el-form-item prop="password" label="密码">
                            <el-input id="password" type="text" v-model="ruleForm.password"  prefix-icon="el-icon-loading" placeholder="输入密码" ></el-input>
                        </el-form-item>
                        
                        
                        <el-form-item>
                            <el-button  style="width:45%;float:left;margin-top:2rem" @click="emptyForm">重置</el-button>
                            <el-button type="primary" style="width:45%;float:right;margin-top:2rem" @click="submitForm('ruleForm')" >登录</el-button>
                        </el-form-item>
                    </el-form>
                    <div style="width:55%;float:right;margin-top:3rem;font-size:18px">没有账户？<a href="/#/register" style="color:#E6A23C">点击登录</a></div>
                </el-col>
                
            </el-row>
        </div>
        </div>
</template>


<script>
import { reactive, onMounted,onBeforeUnmount } from '@vue/composition-api';
import { postInofs } from "../apis/fournight.js";

export default {
    name:'Login',
    components:{},
    setup(props,context){

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

        // 表单验证方法
        const validatePhoneNumber = (rule, value, callback) =>{
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

        const validatePassword = (rule, value, callback) => {
            let passwordreg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$/;
            if (value === '') {
                callback(new Error('密码不能为空'));
            }else if(!passwordreg.test(value)){
                callback(new Error('密码必须：字母、数字; 长度在6到20位之间'))
            } else {
                callback();
            }
            
        };

        const emptyForm = ()=>{
            ruleForm.phoneNumber='';
            ruleForm.password='';
        };

        // 表单内容
        const ruleForm = reactive({  // 更多得想预先设计好了一个容器，去接纳来自当前页面的数据
            phoneNumber: '',
            password: ''
        });

        // 表单验证方法和触发条件
        const rules = reactive({
            phoneNumber: [
                { validator: validatePhoneNumber, trigger: 'blur' } // tirgger 触发规则， blur： 失去焦点的时候触发
            ],
            password: [
                { validator: validatePassword, trigger: 'blur' } // tirgger 触发规则， blur： 失去焦点的时候触发
            ]
        });

        const submitForm = (formName =>{
            context.refs[formName].validate((valid) => {
            // 这个地方的contex表现了，context内大概率就是保存着来自当前页面的信息
            if (valid) {
                alert('submit!');
                const registerData = reactive({
                    url:"/sessions",
                    data:{
                        phoneNumber: ruleForm.phoneNumber,
                        password: ruleForm.password
                        // csrf_token: 
                    }
                });
                console.log(registerData)
                // Register(registerData).then(response => {}).catch(error =>{})
                postInofs(registerData).then((resp) =>{
                    console.log("我就是我，是颜色不一样的烟火： ", resp);
                    // 登录成功，跳转到主页
                    context.root.$router.push("/");
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

        return {
            ruleForm,
            rules,

            emptyForm,
            submitForm
        }
    }
        
}
</script>


<style lang="scss" scoped>
.form{background: rgba(255,255,255,0.3);padding-bottom: 1rem;padding-left: 5rem;padding-right: 5rem;padding-bottom: 1rem;vertical-align: middle;}
    #login_form{display: block;}
    #register_form{display: none;}
    .fa{display: inline-block;top: 27px;left: 6px;position: relative;color: #ccc;}
    input[type="text"],input[type="password"]{padding-left:26px;}
    .checkbox{padding-left:21px;}
</style>