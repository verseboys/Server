<template>
    <div class="e-card-gallery" :style="{
      lineHeight: cardHeight + 'px',
      width: itemsShowCount * cardWidth + 'px',
      height: cardHeight + 'px',
    }">
        <a class="e-card-gallery-btn-prev e-card-gallery-btn"
           @click="moveGalleryByIncrement(1)">
            <span v-if="!$slots['preBtnIcon']"> &lt;</span>
            <slot name="preBtnIcon"></slot>
        </a>
        <div class="e-card-gallery-item-list" ref="itemList">
            <slot></slot>
        </div>
        <a class="e-card-gallery-btn-next e-card-gallery-btn"
           @click="moveGalleryByIncrement(-1)">
            <span v-if="!$slots['nextBtnIcon']"> &gt;</span>
            <slot name="nextBtnIcon"></slot>
        </a>
    </div>
</template>

<script>

import ECardGalleryItem from "./ECardGalleryItem.vue";

import * as Utils from "../common/utils";

export default {
  name: "ECardGallery",
  props: {
    cardWidth: Number | String,
    cardHeight: Number | String,
    itemsShowCount: {
      type: Number | String,
      default: 3
    },
    animateDuration: {
      type: Number | String,
      default: 400
    }
  },

  data() {
    return {
      handleResize: () => this.initalize(),
      isAnimating: false,
      itemsCount: 0,
      currentItemIndex: 0,

    };
  },
  methods: {

    initalize() {
      let items = this.getCardItems();
      this.itemsCount = items.length;
      this.currentItemIndex = 0;
      this.moveGallery(0);
    },
    getTansCSS() {
       return Utils.getTansCSS(this.itemsShowCount);
    },
    getCardItemByIndex(index) {
      return this.getCardItems()[index];
    },
    getCardItems() {
      return ((this.$slots || {}).default || []).filter(
        $slot => $slot && $slot.tag && $slot.tag.indexOf("ECardGalleryItem") > -1
     );
    },

    moveGalleryByIncrement(increment) {
      let currentItemIndex = increment + this.currentItemIndex;
      this.moveGallery(currentItemIndex);
    },

    moveGallery(currentItemIndex) {
      if (this.isAnimating) {
        return;
      }
      let { itemsCount, cardHeight, cardWidth } = this;
      this.isAnimating = true;

      this.currentItemIndex = currentItemIndex;

      if (this.currentItemIndex < 0) {
        this.currentItemIndex = itemsCount - 1;
      }
      if (this.currentItemIndex >= itemsCount) {
        this.currentItemIndex = 0;
      }
      this.resetItemsTransStyle((cssIndex, vnodeIndex) => {
        let vnode = this.getCardItemByIndex(vnodeIndex);
        if (!vnode) {
          return;
        }

        let { componentInstance } = vnode;
        let eCardGalleryItem = componentInstance;
        eCardGalleryItem.setStyle({
          height: `${cardHeight}px`,
          width: `${cardWidth}px`,
          ...this.getTansCSS()[cssIndex]
        });
      });
    this.$emit("swipe", this.currentItemIndex);
    setTimeout(() => {
      this.isAnimating = false;
    }, this.animateDuration); //防止连击
  },

  resetItemsTransStyle(fun) {
    let cssItemCount = this.getTansCSS().length;
    let cardItemCount = this.itemsCount;
    let cssFirstIndex = Math.floor(cssItemCount / 2);
    let itemCardFirstIndex = this.currentItemIndex;
    let cardItemIndexList = [];
    for (let cssIndex = 0; cssIndex < cssItemCount; cssIndex++) {
      let order = cssIndex - cssFirstIndex;
      let itemIndex = itemCardFirstIndex + order;
      if (itemIndex < 0) {
        itemIndex = itemIndex + cardItemCount;
      } else if (itemIndex >= cardItemCount) {
        itemIndex -= cardItemCount;
      }
      cardItemIndexList[cssIndex] = itemIndex;
    }
    cardItemIndexList.map((itemIndex, cssIndex) => {
      fun(cssIndex, itemIndex);
    });
  },

  },

  mounted() {
    this.initalize();
    window.addEventListener("resize", this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.e-card-gallery {
  position: relative;
  display: block;
  height: 100%;
  margin: 0 auto;
}

.e-card-gallery-item-list {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  perspective: 900px;
}
.e-card-gallery-btn {
  position: absolute;
  left: 1%;
  top: 0;
  height: 100%;
  text-align: center;
  vertical-align: middle;
  font-size: 26px;
  width: 8%;
  z-index: 100;
  &.e-card-gallery-btn-next {
    right: 1%;
    left: initial;
  }
}
</style>
