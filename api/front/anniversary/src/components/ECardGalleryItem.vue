<!--suppress JSAnnotator -->
<template>
    <div class="e-card-gallery-item"
    @click="handleClickCardItem"
    :style="style">
        <slot></slot>
    </div>
</template>

<script>
export default {
  name: "ECardGalleryItem",

  props: {
    order: Number,
    theme: String
  },
  data() {
    return {
      style: {

      }
    };
  },
  methods: {
    setStyle(style) {
      let { theme } = this;
      if (theme === "primary") {
        style = { backgroundColor: "#2196F3", color: "#fff", ...style };
      }
      this.style = style;
    },
    handleClickCardItem(evt) {
      this.$parent.moveGallery(this.order);
    }
  },

}
</script>

<style scoped lang="less">
.e-card-gallery-item {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 0;
  padding: 0;
  display: block;
  opacity: 0;
  visibility: hidden;
  transition: all 0.4s ease-in-out 0s;
  /* box-shadow: 0px 2px 0px 0px rgba(0, 0, 0, 0.2),
    0px 1px 1px 0px rgba(0, 0, 0, 0.14), 0px 1px 3px 0px rgba(0, 0, 0, 0.12); */
}
</style>
