<template>
    <div style="background-color: #475DD9;">
    <e-card-gallery
    @swipe="handleMoveGallery"
    card-width="345" card-height="246" >
      <a-icon type="left" slot="preBtnIcon" theme="filled"/>
      <e-card-gallery-item v-for="(item, order) in friends" :key="item.name">
        <e-friend-card v-bind="item" :order="order" :currentFriendIndex="currentFriendIndex"/>
      </e-card-gallery-item>
      <a-icon type="right" slot="nextBtnIcon" theme="filled"/>
  </e-card-gallery>
  </div>
</template>

<script>

import EFriendCard from "./EFriendCard.vue";

const {
    ECardGallery,
    ECardGalleryItem
} = require("/home/yiliu/workspace/e-card-gallery/dist/eCardGallery.umd.js").default;

import { friends } from "../configs";
export default {
  name: 'EFriends',
  data () {
    return {
      currentFriendIndex: 0,
      friends
    }
  },
  components: {
    ECardGallery,
    ECardGalleryItem,
    EFriendCard
  },
  methods:{
    handleMoveGallery(currentIndex) {
      this.currentFriendIndex = currentIndex;
    }
  },
  created:function(){

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
a.e-card-gallery-btn {
  color: #94a1f8;
}
</style>
