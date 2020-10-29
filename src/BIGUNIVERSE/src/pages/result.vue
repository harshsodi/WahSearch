<template>
  <div class="result-page">
    <el-row :gutter="0" class="page-header">
      <span class="title-text" @click="()=>{this.$router.push(`/home`)}">WAH SEARCH</span>
      <el-autocomplete @keyup.enter.native="handleSearchFromInput()" class="inline-input" v-model="searchText" :fetch-suggestions="querySearch" placeholder="" :trigger-on-focus="false">
        <el-button @click="handleSearchFromInput()" slot="append" icon="el-icon-search"></el-button>
      </el-autocomplete>
    </el-row>

    <div class="result-flex">
      <div class="result-box">
        <div class="result-num">About <span v-text="this.totalSize"></span> links here</div>

        <br>

        <resultBoxList :resultList="displayList[selectedMenu]"></resultBoxList>

        <br>

        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="pageNum" :page-sizes="[10, 30, 50, 100, 300, 500]" :page-size="pageSize" layout="total, sizes, prev, pager, next" :total="totalSize">
        </el-pagination>
        <br>
        <br>
        <br>
        <br>
        <br>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

import { Loading } from 'element-ui';

import resultBoxList from '@/components/resultList'

export default {
  components: {
    resultBoxList,
  },
  data() {
    return {
      searchText: null,
      // result: null,
      selectedMenu: "all",
      // resultList: [],
      totalSize: 0,
      totalAll: 0,
      pageNum: 1,
      pageSize: 20,
      displayList: {
        all: [],
        commonInfo: [],
        system: [],
        process: [],
        knowledge: [],
      },
      recommendList: [],
      recommendList2: [],

    }
  },
  created() {
    // console.log(this.$route.params.searchText)

    this.searchText = this.$route.params.searchText

    this.handleSearch()
  },
  mounted() {
    this.queryList = this.loadAll();
  },
  methods: {
    handleSizeChange(val) {
      console.log(` ${val} links`);
      this.pageSize = val
      this.handleSearch()
    },
    handleCurrentChange(val) {
      console.log(` ${val}`);
      this.pageNum = val
      this.handleSearch()
    },

      querySearch(queryString, cb) {
          axios.get(`/suggestion`, {
              params: {
                  keywords: this.searchText.trim(),
              }
          }).then(res => {
              if (!res.data) {
                  this.$alert("ERROR")
              } else {
                  console.log("get suggestion = " + res.data)
                  var dic = [{}];
                  for (let i of res.data) {
                      dic.push({value: i})
                  }
                  cb(dic)
              }
          })
      },
    handleSelect(index, indexPath) {
      this.selectedMenu = index
      this.totalSize = index == 'all' ? this.totalAll : this.displayList[index].length
    },
    handleSearchFromInput() {
      this.pageNum = 1
      this.pageSize = 10
      this.handleSearch()
    },
    handleSearch() {
      // console.log("searchText", this.searchText)
      if (!this.searchText.trim().length) {
        this.$message.warning("there is no words")
        return
      }
      this.$router.push(`/result/${this.searchText.trim()}`)
      let fullScreenLoading = Loading.service({ fullscreen: true });
      axios.get(`/search`, {
        params: {
            keywords: this.searchText.trim(),
            page_number: this.pageNum,
            per_page: this.pageSize
        }
      }).then(res => {
        if (!res.data) {
          this.$alert("ERROR")
          fullScreenLoading.close()
        } else {
          fullScreenLoading.close()
          //  res.data.data
          console.log(res.data)

          this.displayList.all = res.data.links
          console.log(this.displayList.all)
          this.totalSize = res.data.total_links
          this.totalAll = res.data.links.length

          this.selectedMenu = 'all'

        }
      })

    },

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
 <style lang="less">
.result-page {
  // height: 100%;
  .page-header {
    padding: 0px 10px;
    // padding-top: 10px;
    // line-height: 60px;
    text-align: left;
    border-bottom: 1px solid #cecece;
    height: 60px;
    display: flex;
    // flex-direction: column;
    // justify-content: flex-start;
    // align-items: center;
    .title-text {
      width: 150px;
      // order: 1;
      font-size: 20px;
      color: darkblue;
      font-weight: bold;
      line-height: 60px;
    }
    .inline-input {
      margin-top: 10px;
      // flex: 1;
      width: 600px;
    }
  }
  .el-menu.el-menu--horizontal {
    padding-left: 160px;
    background-color: mix(#ffffff, #000000, 95%);
  }
  .el-menu--horizontal > .el-menu-item {
    height: 40px;
    line-height: 40px;
  }
  .result-flex {
    display: flex;
    justify-content: flex-start;
    // height: 100%;
    .result-box {
      margin-top: 20px;
      margin-left: 160px;
      width: 600px;
      .result-num {
        font-size: 12px;
        color: #999;
      }
    }
    .result-recommend {
      margin-top: 50px;
      margin-left: 100px;
      padding-left: 90px;
      width: 440px;
      min-height: calc(100% - 300px);
      border-left: 1px solid #e1e1e1;
    }
  }
}
</style>
