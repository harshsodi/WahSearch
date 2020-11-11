<template>
  <div>
    <div class="result-item" v-for="(item,index) in resultList" :key="index">
      <!-- {{item}} -->

      <div>
        <div class="item-title"><a target="_blank" :href="item.url"><span v-html="item.title" /></a></div>
        <div class="item-link"><a target="_blank" :href="item.url">{{item.url}} </a>  </div>
      </div>

      <br>
    </div>
  </div>

</template>
<script>

export default {
  data() {
    return {

    }
  },
  props: ["resultList"],
  created() {
    // console.log(resultList)
  },

}
</script>
<style lang="less">
.result-item {
  font-family: arial;
  font-size: 13px;
  line-height: 1.54;
  font {
    color: red;
  }
  .bus-title {
    font-weight: bold;
    font-size: 18px;
    line-height: 24px;
    color: chocolate;
  }
  .collapse-title {
    font-size: 16px;
    width: 100%;
  }
  .el-collapse-item__header {
    min-height: 36px;
    line-height: 24px;
    padding: 5px 0px;
  }
  .align-right {
    text-align: right;
  }
  .card-title {
    font-size: 17px;
    line-height: 15px;
    font-weight: 400;
  }
  .item-title {
    font-size: 17px;
    line-height: 20px;
    font-weight: 400;
    margin-bottom: 4px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    overflow: hidden;
  }
  .item-content {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
  }
  .item-link {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    overflow: hidden;
    a {
      text-decoration: none;
      color: green;
      word-break: break-all;
      // word-wrap: break-word;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 1;
      overflow: hidden;
    }
  }
}
</style>

