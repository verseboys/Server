<template>
<div  class = "common_container" >
    <div class="common_center_container">
        <a-row class="common_mid_title_container" align="middle" type="flex" justify="center">
            <a-col :span="8" class="height-50 common_annex_container"><div class="common_annex1"></div><div class="common_annex2"></div></a-col>
            <a-col :span="8" class="height-50 "><div class="common_title">优秀的小伙伴们</div></a-col>
            <a-col :span="8" class="height-50 "><div class="common_annex3"></div><div class="common_annex4"></div></a-col>
        </a-row>
        <div style="background-color: #475DD9;">
          <e-card-gallery
          @swipe="handleMoveGallery"
          card-width="345" card-height="246" >
            <a-icon type="left" slot="preBtnIcon" theme="filled"/>
            <e-card-gallery-item v-for="(item, order) in friends"
            :order="order"
            :key="item.name">
              <e-friend-card v-bind="item" :order="order"/>
            </e-card-gallery-item>
            <a-icon type="right" slot="nextBtnIcon" theme="filled"/>
          </e-card-gallery>
        </div>
    </div>
</div>
</template>

<script>

import EFriendCard from "./EFriendCard.vue";

import { friends } from "../constants";

import ECardGallery from "./ECardGallery.vue";
import ECardGalleryItem from "./ECardGalleryItem.vue";

export default {
  name: 'ECardGalleryInstance',
  data () {
    return {
      friends
    }
  },
  components: {
    ECardGallery,
    ECardGalleryItem,
    EFriendCard,
  },
  created:function(){

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
.common_container{
  min-height:660px
}
.common_mid_title_container{
  margin-bottom:150px
}
a.e-card-gallery-btn {
  color: #94a1f8;
}
</style>
