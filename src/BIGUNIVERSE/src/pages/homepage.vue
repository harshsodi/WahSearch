<template>
  <div class="homepage" style="text-align: center;">
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <h1 class="title-text">WAH SEARCH</h1>
    <br>
    <br>
    <br>
    <el-row :gutter="0" style="text-align: center">
      <el-col :span="6">&nbsp;</el-col>
      <el-col :span="12">
        <el-autocomplete @keyup.enter.native="handleSearch()" class="inline-input" v-model="searchText"
                         :fetch-suggestions="querySearch" placeholder="search something..." :trigger-on-focus="false">
          <el-button @click="handleSearch()" slot="append" icon="el-icon-search"></el-button>
        </el-autocomplete>
      </el-col>
      <el-col :span="6">&nbsp;</el-col>
    </el-row>
    <br>
    <br>
    <br>
  </div>
</template>

<script>
    import axios from "axios";

    export default {

        data() {
            return {
                searchText: null,
                webList: [
                    {
                        title: "",
                        url: "",
                    }
                ]
            }
        },
        mounted() {
        },
        methods: {
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
                        console.log("get dic = " + dic.length)
                        if (dic.length == 1) {
                            cb([{value: "there is no suggestion"}])
                        } else {
                            cb(dic)
                        }
                    }
                })
            },
            handleSelect(item) {
                // console.log(item);
            },
            handleSearch() {
                //
                console.log("searchText", this.searchText.length, this.searchText.trim().length)
                if (!this.searchText.trim().length) {
                    this.$message.warning("there is no words")
                    return
                }
                this.$router.push(`/result/${this.searchText}`)
            }
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
  .homepage {
    /* background: linear-gradient(#fff, #409eff); */
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    min-width: 1400px;
    /* z-index: -10; */
    zoom: 1;
    background-color: #fff;
    background-image: url("../../static/background.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    /* -webkit-background-size: cover; */
    /* -o-background-size: cover; */
    background-position: center 0;
    /* height: 100%; */
    /* min-width: 1200px; */

    .title-text {
      font-size: 70px;
      /* margin-top: 13px; */
      color: #ffffff;
      /* text-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
      // text-shadow: 0px 0px 6px #ffffff;
      /* box-shadow:  */
    }

    .el-autocomplete {
      width: 100%;
    }
  }
</style>
