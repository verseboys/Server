<template>

  <div class="e-friend-card" :class="cls">
    <div class="e-friend-card-firstline">
    <img class="e-friend-card-avatar"
     :src="avatar" :alt="title"/>
    <div class="e-friend-card-title">
        {{title}}
    </div>
    <div class="e-friend-card-subtitle" v-html="subtitle"></div>

    <div class="e-friend-card-divider">
    </div>
    </div>
    <div class="e-friend-card-detail" :title="detail">
      {{detail}}
    </div>
  </div>
</template>

<script>
export default {
  name: 'EFriendCard',
  props: {
    order: Number,
    title: String,
    subtitle: String,
    detail: String,
    name: String
  },
  components: {

  },
  data () {
    let { order } = this;
    let cls = `e-friend-card-group-${order % 3}`;
    return {
      cls,
      avatar: `/anniversary_static/img/friends/${this.name}.jpg`,
    }
  },
  components: {

  },
  methods:{
  },
  computed: {
    visible() {
      let { name, currentIndex, order} = this;
      console.log(name, currentIndex, order);
      // return Math.abs(currentIndex - order) > 4 ? 'hidden' : "visible";
    }
  },
  created:function(){

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">


.e-friend-card {
  padding: 40px 30px 32px 27px;
  width: 100%;
  height: 100%;
  position: relative;
  display: block;
  box-shadow: -4px 0 4px 0 rgba(0,0,0,0.12), 4px 0 6px 0 rgba(7,7,7,0.19);
  border-radius: 8px;
  line-height: 1;
  text-align: left;
  color: #fff;

  .e-friend-card-detail {
    font-size: 13px;
    line-height: 1.92;
  }

  &.e-friend-card-group-2 {
    background-image: linear-gradient(130deg, #b779e7, #8264e1);
  }

  &.e-friend-card-group-0 {
    background-image: linear-gradient(-133deg, #4BB9F9 0%, #216DCE 100%);
  }

  &.e-friend-card-group-1 {
    background-image: linear-gradient(125deg, #9fe3dc, #59c2d7);
    // background-image: linear-gradient(1deg, #475ad7, #446cdb);
  }
  .e-friend-card-title {
    font-weight: 500;
    font-size: 28px;
    padding-bottom: 9px;
  }
  .e-friend-card-subtitle {
    font-size: 14px;
    line-height: 1.57;
    height: 51px;
  }
  img.e-friend-card-avatar {
    width: 85px;
    height: 85px;
    display: block;
    border-radius: 50%;
    position: absolute;
    left: 21px;
    top: 32px;
}

.e-friend-card-divider {
  // margin-left: -15px;
  // height: 3px;
  opacity: 0.3;
  background-color: #ffffff;
  border-bottom: solid 1px transparent;
}

.e-friend-card-firstline {
    padding-left: 97px;
    margin-bottom: 14px;
}

.e-friend-card-detail {
    overflow: hidden;
    height: 74px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

}

</style>
