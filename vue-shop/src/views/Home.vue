<template>
<div class="home" id="home" name="home">
    <div class="block">
      <el-carousel height="460px">
        <el-carousel-item v-for="item in 6" :key="item.carousel_id">
          <img style="height:460px;" src="/images/register_background" alt="" />
        </el-carousel-item>
      </el-carousel>
    </div>
    <!-- 轮播图END -->

    <div class="main-box">
      <div class="main">
        <!-- 手机商品展示区域 -->
        <div class="phone">
          <div class="box-hd">
            <div class="title">手机</div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <router-link to>
                <img src="/test-images/phone.png" />
              </router-link>
            </div>
            <div class="list">
              <!-- <MyList :list="phoneList" :isMore="true"></MyList> -->
            </div>
          </div>
        </div>
        <!-- 手机商品展示区域END -->

        <!-- 家电商品展示区域 -->
        <!-- <div class="appliance" id="promo-menu">
          <div class="box-hd">
            <div class="title">家电</div>
            <div class="more" id="more">
              <MyMenu :val="2" @fromChild="getChildMsg">
                <span slot="1">热门</span>
                <span slot="2">电视影音</span>
              </MyMenu>
            </div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <ul>
                <li>
                  <img :src="$target +'public/imgs/appliance/appliance-promo1.png'" />
                </li>
                <li>
                  <img :src="$target +'public/imgs/appliance/appliance-promo2.png'" />
                </li>
              </ul>
            </div>
            <div class="list">
              <MyList :list="applianceList" :isMore="true"></MyList>
            </div>
          </div>
        </div> -->
        <!-- 家电商品展示区域END -->

        <!-- 配件商品展示区域 -->
        <!-- <div class="accessory" id="promo-menu">
          <div class="box-hd">
            <div class="title">配件</div>
            <div class="more" id="more">
              <MyMenu :val="3" @fromChild="getChildMsg2">
                <span slot="1">热门</span>
                <span slot="2">保护套</span>
                <span slot="3">充电器</span>
              </MyMenu>
            </div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <ul>
                <li>
                  <img :src="$target +'public/imgs/accessory/accessory-promo1.png'" alt />
                </li>
                <li>
                  <img :src="$target +'public/imgs/accessory/accessory-promo2.png'" alt />
                </li>
              </ul>
            </div>
            <div class="list">
              <MyList :list="accessoryList" :isMore="true"></MyList>
            </div>
          </div>
        </div> -->
        <!-- 配件商品展示区域END -->
      </div>
    </div>

     
</div>
</template>

<script>
import { reactive, ref } from '@vue/composition-api';

// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Home",
  components: {
    
  },
  setup(props, context){

    

    
    const activeIndex2=ref('1');

    const handleSelect= (key, keyPath) =>{
        console.log(key, keyPath);
      }


    return {
      activeIndex2,

      handleSelect
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../assets/css/index.css";
</style>
