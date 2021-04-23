<template>
  <!-- 容器 -->
  <div class="moduleListContainer">
    <div class="moduleListContent">

      <!-- 导航 -->
      <div class="moduleListNav">
        <!-- 标题 -->
        <h4 class="m0 moduleListTitle">巡检对象：</h4>
        <!-- /标题 -->

        <!-- content -->
        <div style="flex: 1;" class="flexBox" :class="{ 'collapsed': isCollapse }">
          <div class="navItem mr15 allTag" :class="{ 'active': activeId === 0 }" @click="handleSearchAll">全部</div>

          <div
            class="navItem mr15"
            v-for="v in $store.getters.getOsList"
            :key="v.id"
            :class="{ 'active': v.id === activeId }"
            @click="handleFilterOs(v)">
            {{ v['os_name'] }}
          </div>
        </div>
        <!-- /content -->

        <!-- 展开收缩按钮-->
        <div class="moduleListNavCollapse" @click="handleCollapse">
          {{ isCollapse ? '展开' : '收缩'}}
          <bk-icon :type="isCollapse ? 'angle-right' : 'angle-down'" />
        </div>
        <!-- /展开收缩按钮-->
      </div>
      <!-- /导航 -->

      <!-- 列表 -->
      <div class="listContainer" v-bkloading="{ isLoading: isLoading, zIndex: 10 }">
        <bk-container :col="12">
          <bk-row>
            <bk-col :span="$store.getters.getTplColSpan" v-for="v in tplList" :key="v.id">

              <!-- 新增按钮 -->
              <div v-if="v.hasOwnProperty('isAddBtn')" class="addModuleBtnContainer listItem" @click="handleAddTpl">
                +
              </div>
              <!-- /新增按钮 -->

              <!-- 卡片 -->
              <div v-else class="listItem" @click="handleCheckDetail(v)">
                <!-- 图片 -->
                <div class="listItemTop">
                  <img
                    style="width: 100%; height: 100%;"
                    :src="`${$store.getters.getImgFilePath}${v['tpl_os_name'].split('/')[v['tpl_os_name'].split('/').length - 1]}.png`"
                    alt="">
                </div>
                <!-- /图片 -->

                <!-- content -->
                <div class="listItemBottom">
                  <div>
                    <!-- 模板名称 -->
                    <h5 class="m0 tplNameContainer" v-bk-tooltips.top-start="v['tpl_name']">
                      {{ v['tpl_name'] }}
                    </h5>
                    <!-- /模板名称 -->

                    <!-- 模板描述 -->
                    <div class="fontStyle mt5">
                      <bk-popover :placement="'top-start'" width="230">
                        <div class="descriptionContainer">{{ v.description }}</div>
                        <div slot="content" style="word-break: break-all;">
                          {{ v.description }}
                        </div>
                      </bk-popover>
                    </div>
                    <!-- /模板描述 -->
                  </div>

                  <!-- 复制删除按钮 -->
                  <div class="flexBox" style="justify-content: space-between">
                    <div class="fontStyle">{{ v['created_time'] }}</div>
                    <div class="listItemBtn" v-show="v['author'] !== 'system'">
                      <span class="p5" @click.prevent.stop="handleEditTpl(v)">复制</span>
                      <span class="p5" @click.prevent.stop="handleDelTpl(v)">删除</span>
                    </div>
                  </div>
                  <!-- /复制删除按钮 -->
                </div>
                <!-- /content -->
              </div>
              <!-- /卡片 -->
            </bk-col>
          </bk-row>
        </bk-container>
      </div>
      <!-- /列表 -->
    </div>
  </div>
  <!-- /容器 -->
</template>

<script>
    export default {
        name: 'list',

        data () {
            return {
                isLoading: false,
                activeId: 0,
                tplList: [],
                isCollapse: true
            }
        },

        created () {
            this.fetch_tpl_list()
        },

        methods: {
            handleCollapse () {
                this.isCollapse = !this.isCollapse
            },
            // 查询所有模板
            handleSearchAll () {
                this.activeId = 0
                this.fetch_tpl_list()
            },
            // 查询指定模板
            handleFilterOs (param) {
                const { id } = param
                this.activeId = id

                const params = { id }
                this.fetch_tpl_list(params)
            },
            // 查询模板
            async fetch_tpl_list (params = {}) {
                const { keys } = Object
                const queryData = {}
                if (keys(params).length !== 0) {
                    queryData['os_id'] = params.id
                }

                try {
                    this.isLoading = true
                    this.tplList = [{ isAddBtn: true }]
                    const res = await this.$store.dispatch('fetch_tpl_list', queryData)
                    const { data } = res
                    data.forEach(item => this.tplList.push(item))
                } catch (e) {
                    console.log('fetch_tpl_list=', e)
                } finally {
                    this.isLoading = false
                }
            },
            // 新增
            handleAddTpl () {
                this.$router.push({
                    name: 'moduleAdd'
                })
            },
            // 查看详情
            handleCheckDetail (param) {
                const { id } = param

                this.$router.push({
                    name: 'moduleDetail',
                    query: { id }
                })
            },
            // 复制
            handleEditTpl (param) {
                const { id, tpl_os } = param
                const query = {
                    id,
                    tpl_os
                }

                // if (param['related_task'].length > 0) {
                //     const tasksStr = param['related_task'].map(item => `【${item['task_name']}】`).join('')
                //     const subTitle = `该模板目前已被引用于${tasksStr}，编辑后上述任务也将变更，是否继续？`
                //
                //     return this.$bkInfo({
                //         theme: 'warning',
                //         title: '确认要编辑？',
                //         subTitle,
                //         okText: '继续编辑',
                //         confirmFn: () => this.handleJumpRouter(query)
                //     })
                // }

                this.handleJumpRouter(query)
            },
            handleJumpRouter (query) {
                this.$router.push({
                    name: 'moduleAdd',
                    query
                })
            },

            // 删除
            handleDelTpl (param) {
                const params = {
                    tpl_id: param.id
                }

                let isCanDel = true
                let subTitle = '该模板目前未被引用于任何任务，且之前所产生的报告不会被删除，【历史报告列表】中支持查阅，是否确认删除？'
                let okText = '确认删除'
                let theme = 'danger'
                const title = '确认要删除？'

                if (param['related_task'].length > 0) {
                    const tasksStr = param['related_task'].map(item => `【${item['task_name']}】`).join('')
                    subTitle = `该模板目前已被引用于${tasksStr}，不支持删除！`
                    okText = '确认'
                    isCanDel = false
                    theme = 'primary'
                }

                this.$bkInfo({
                    theme,
                    title,
                    subTitle,
                    okText,
                    confirmLoading: true,
                    confirmFn: async () => {
                        if (isCanDel) return this.tpl_delete(params)

                        return true
                    }
                })
            },
            async tpl_delete (params = {}) {
                try {
                    const res = await this.$store.dispatch('tpl_delete', params)
                    const { code, message } = res
                    const theme = code === 0 ? 'success' : 'error'
                    this.$bkMessage({ delay: 3000, message, theme })

                    const queryData = {}
                    const { activeId } = this
                    if (activeId !== 0) queryData.id = activeId
                    await this.fetch_tpl_list(queryData)
                } catch (e) {
                    console.log('tpl_delete=', e)
                }
            }
        }
    }
</script>

<style lang="postcss" scoped>
  .moduleListContainer {
    padding: 20px;

    .flexBox {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
    }

    .fontStyle {
      font-size: 12px;
      color: #ccc;
    }

    .moduleListNav {
      background: #ffffff;
      border-radius: 6px;
      display: flex;
      padding: 10px 20px;
      justify-content: space-between;

      .collapsed {
        display: flex;
        align-items: center;
        flex-wrap: nowrap;
        overflow: hidden;
      }

      .moduleListTitle {
        min-width: 90px;
        height: 36px;
        line-height: 36px;
      }

      .allTag {
        min-width: 60px;
        text-align: center;
      }

      .navItem {
        cursor: pointer;
        height: 36px;
        line-height: 36px;
        padding: 0 8px;
        border-radius: 3px;
        margin-bottom: 5px;
      }

      .active {
        background: #1d91ec;
      }

      .moduleListNavCollapse {
        height: 36px;
        min-width: 60px;
        display: flex;
        align-items: center;
        justify-content: space-around;
        cursor: pointer;
        color: #1d91ec;

      }
    }

    .listContainer {
      margin: 20px 0;
      background: #ffffff;
      padding: 20px;

      .addModuleBtnContainer {
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: #ccc;
        font-size: 70px;
      }

      .listItem {
        width: 250px;
        height: 260px;
        border: 1px solid #ccc;
        background: #FFFFFF;
        box-shadow: 4px 4px 6px #ccc;
        cursor: pointer;
        margin: 0 auto 20px auto;

        .listItemTop {
          height: 60%;
          width: 100%;
        }

        .listItemBottom {
          width: 100%;
          height: 40%;
          padding: 10px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;

          .tplNameContainer {
            height: 18px;
            line-height: 18px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 1;
            word-break: break-all;
          }

          .descriptionContainer {
            height: 32px;
            line-height: 16px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 2;
            word-break: break-all;
          }

          .listItemBtn {
            color: #1d91ec;
            font-size: 12px;
          }
        }
      }
    }
  }
</style>
