<template>
  <div class="select-server">
    <bk-dialog v-model="dialogVisible"
               ext-cls="select-server-dialog-container"
               width="940"
               :position="positionArr"
               theme="primary"
               :mask-close="false"
               :draggable="false"
               :close-icon="false">
      <div class="select-server-dialog-box">
        <bk-tab :active.sync="active">
          <bk-tab-panel name="1" label="静态 - IP 选择">
            <div class="topology-data-box">
              <div class="search-div">
                <bk-input :right-icon="'bk-icon icon-search'" @change="handleTopoValChange" v-model="searchWord" placeholder="搜索 拓扑节点" />
              </div>
              <div class="tree-box" v-bkloading="{ isLoading: isTreeLoading, zIndex: 10 }">
                <bk-tree
                  ref="topoTree"
                  style="padding: 0;"
                  :data="treeList"
                  :node-key="'id'"
                  :has-border="true"
                  @on-click="handleNodeClick"
                  @on-expanded="handleNodeExpanded">
                </bk-tree>
                <div v-show="isEmpty" style="color: #c4c6cc;">未匹配到相关数据</div>
              </div>
            </div>
            <div class="host-list-box">
              <!--<bk-input
                style="width: 503px;"
                ext-cls="fl"
                :placeholder="'输入 主机IP 按Enter进行过滤...'"
                :right-icon="'bk-icon icon-search'"
                v-model.trim="keywords"
                @enter="handleSearch">
              </bk-input>
              <bk-button ext-cls="ml10 mb20 fl" theme="primary" @click.stop.prevent="handleSearch" :loading="isChecking">搜索</bk-button>-->
              <bk-table
                ref="multipleTableSelect"
                :data="hostTableData"
                :outer-border="true"
                :header-border="false"
                v-bkloading="{ isLoading: isTableLoading, zIndex: 10 }"
                @select="handleRowSelect"
                @select-all="handleAllSelect"
                @selection-change="handleSelectHosts">
                <bk-table-column type="selection" width="60"></bk-table-column>
                <bk-table-column label="主机IP" prop="bk_host_innerip"></bk-table-column>
                <bk-table-column label="云区域" prop="bk_cloud_id"></bk-table-column>
                <bk-table-column label="主机名" prop="bk_host_name"></bk-table-column>
                <bk-table-column label="操作系统" prop="bk_os_name"></bk-table-column>
              </bk-table>
            </div>
          </bk-tab-panel>

          <bk-tab-panel name="2" disabled label="动态 - 拓扑选择">
            动态 - 拓扑选择
          </bk-tab-panel>
          <bk-tab-panel name="3" disabled label="动态 - 分组选择">
            动态 - 分组选择
          </bk-tab-panel>
          <bk-tab-panel name="4" disabled label="手动输入">
            手动输入
          </bk-tab-panel>
        </bk-tab>
      </div>
      <div slot="footer">
        <bk-button ext-cls="mr10" theme="primary" @click="handleConfirm" :loading="isChecking">确定</bk-button>
        <bk-button theme="default" @click="handleUpdateDialogVisible({ isShow: false, type: 'cancel' })">取消</bk-button>
      </div>
    </bk-dialog>
  </div>
</template>

<script>
    import http from '@/api'
    // import { bus } from '@/common/bus'

    export default {
        name: 'app-select-server',
        components: {},
        data () {
            return {
                dialogVisible: false, // 选择服务器弹窗
                active: '1',
                positionArr: {
                    top: 100
                },
                isEmpty: false,
                timer: null, // 防抖函数定时器
                searchWord: '', // 搜索拓扑节点关键字
                treeList: [], // 拓扑节点树list
                topoNodeData: {}, // 选中拓扑节点data
                keywords: '',
                hostTableData: [],
                selectHostList: [],
                isChecking: false,
                isTreeLoading: false,
                bk_biz_id: null,
                isTableLoading: false,
                activeTopoName: '',
                hostSelectedData: {},
                currentNodeData: {},
                topTopoName: '',
                osId: null
            }
        },
        created () {},
        mounted () {},
        methods: {
            // 打开选择服务器弹窗
            opDialogPop (params = {}) {
                const { osId } = params
                this.osId = osId

                const updateConfig = {
                    isShow: true,
                    type: 'show'
                }
                this.handleUpdateDialogVisible(updateConfig)

                this.getBizInstTopo(params)
            },

            // 获取拓扑树data
            async getBizInstTopo (params) {
                try {
                    this.isTreeLoading = true
                    const { id } = params
                    this.bk_biz_id = id
                    const url = `/api/business_hosts?bk_biz_id=${id}`
                    const res = await http.get(url)
                    const { data } = res

                    if (data) data.selected = true

                    this.treeList.push(data)

                    if (data) {
                        const { bk_obj_id, bk_inst_id, name } = data
                        this.currentNodeData = data

                        await this.handleUpdateActiveTopoName(name)
                        this.topTopoName = name
                        const { activeTopoName } = this
                        this.hostSelectedData[activeTopoName] = []

                        const param = {
                            bk_obj_id,
                            bk_inst_id,
                            bk_biz_id: id
                        }
                        await this.handleFetchIpByTopo(param)

                        const originalHostsResult = await this.$parent.handleReturnOriginalResult()
                        if (originalHostsResult) {
                            this.hostSelectedData[activeTopoName] = originalHostsResult
                            this.hostSelectedData[this.topTopoName] = originalHostsResult
                            this.setHostSelected()
                        }
                    }
                } catch (e) {
                    console.error(e)
                } finally {
                    this.isTreeLoading = false
                }
            },

            // 搜索 拓扑节点input框内容改变 搜索拓扑节点
            handleTopoValChange (value) {
                this.throttle(this.search, 400)
            },

            // 左侧拓扑树筛选查找
            search () {
                this.$refs.topoTree.searchNode(this.searchWord)
                const searchResult = this.$refs.topoTree.getSearchResult()
                this.isEmpty = searchResult.isEmpty
            },

            // 点击拓扑节点
            async handleNodeClick (node) {
                const { bk_obj_id, bk_inst_id, name, parent } = node
                this.currentNodeData = node

                if (this.activeTopoName === name) return

                await this.handleUpdateActiveTopoName(name)

                const { bk_biz_id } = this
                const params = {
                    bk_biz_id,
                    bk_obj_id,
                    bk_inst_id
                }

                await this.handleFetchIpByTopo(params)

                await this.setHostSelected(parent)
            },

            async handleFetchIpByTopo (params = {}) {
                try {
                    this.isTableLoading = true
                    const { osId } = this
                    const paramsStr = `?bk_biz_id=${params['bk_biz_id']}`
                        + `&bk_obj_id=${params['bk_obj_id']}`
                        + `&bk_inst_id=${params['bk_inst_id']}`
                        + `&os_id=${osId}`
                    const res = await http.get(`/api/hosts_topo${paramsStr}`)
                    const { data } = res
                    this.hostTableData = data
                } catch (e) {
                    console.error(e)
                } finally {
                    this.isTableLoading = false
                }
            },

            // node节点展开收起
            handleNodeExpanded (node, expanded) {},
            // 根据拓扑信息搜索主机列表
            searchHostList (val) {},
            handleSearch () {},

            handleSelectHosts (selection) {
                this.$nextTick(() => {
                    // const { activeTopoName } = this
                    // if (activeTopoName) this.hostSelectedData[activeTopoName] = [...selection]

                    // const { topTopoName, hostSelectedData } = this
                    // if (topTopoName) {
                    //     this.hostSelectedData[topTopoName] = hostSelectedData[topTopoName].concat([...selection])
                    // }
                })
            },
            handleRowSelect (selection) {
                this.$nextTick(() => {
                    const { hostTableData, topTopoName, hostSelectedData } = this

                    const selectionList = [...selection]

                    // 获取未选中数据
                    let notSelectedList = []
                    if (selectionList.length === 0) notSelectedList = hostTableData

                    hostTableData.forEach(data => {
                        selectionList.forEach(selected => {
                            if (data['bk_host_innerip'] !== selected['bk_host_innerip']) {
                                notSelectedList.push(data)
                            }

                            if (notSelectedList.length !== 0) {
                                // notSelectedList.forEach(() => {
                                //     notSelectedList = notSelectedList.filter(item => {
                                //         return item['notSelected'] !== selected['bk_host_innerip']
                                //     })
                                // })
                                notSelectedList = notSelectedList.filter(item => {
                                    return item['notSelected'] !== selected['bk_host_innerip']
                                })
                            }
                        })
                    })

                    notSelectedList.forEach(notSelected => {
                        this.hostSelectedData[topTopoName] = hostSelectedData[topTopoName].filter(host => {
                            return host['bk_host_innerip'] !== notSelected['bk_host_innerip']
                        })
                    })

                    if (selectionList.length !== 0) {
                        this.hostSelectedData[topTopoName] = hostSelectedData[topTopoName].concat(selectionList)
                    }

                    // if (currentNodeData.parent) {
                    //     const selectionList = [...selection]
                    //
                    //     // 获取未选中数据
                    //     let notSelectedList = []
                    //     if (selectionList.length === 0) notSelectedList = hostTableData
                    //
                    //     hostTableData.forEach(data => {
                    //         selectionList.forEach(selected => {
                    //             if (data['bk_host_innerip'] !== selected['bk_host_innerip']) {
                    //                 notSelectedList.push(data)
                    //             }
                    //
                    //             if (notSelectedList.length !== 0) {
                    //                 notSelectedList.forEach(() => {
                    //                     notSelectedList = notSelectedList.filter(item => item['notSelected'] !== selected['bk_host_innerip'])
                    //                 })
                    //             }
                    //         })
                    //     })
                    //
                    //     // 重新赋值对应父级选中数据
                    //     notSelectedList.forEach(notSelected => {
                    //         this.hostSelectedData[currentNodeData.parent.name] = this.hostSelectedData[currentNodeData.parent.name].filter(host => {
                    //             return host['bk_host_innerip'] !== notSelected['bk_host_innerip']
                    //         })
                    //     })
                    //
                    //     if (selectionList.length !== 0) {
                    //         this.hostSelectedData[currentNodeData.parent.name] = this.hostSelectedData[currentNodeData.parent.name].concat(selectionList)
                    //     }
                    // }
                })
            },
            handleAllSelect (selection) {
                this.$nextTick(() => {
                    const { hostTableData, topTopoName, hostSelectedData } = this

                    const selectionList = [...selection]

                    // 获取未选中数据
                    let notSelectedList = []

                    if (selectionList.length !== 0) notSelectedList = []

                    if (selectionList.length === 0) notSelectedList = hostTableData

                    notSelectedList.forEach(notSelected => {
                        this.hostSelectedData[topTopoName] = hostSelectedData[topTopoName].filter(host => {
                            return host['bk_host_innerip'] !== notSelected['bk_host_innerip']
                        })
                    })

                    if (notSelectedList.length === 0) {
                        this.hostSelectedData[topTopoName] = hostSelectedData[topTopoName].concat(selectionList)
                    }

                    // if (currentNodeData.parent) {
                    //     const selectionList = [...selection]
                    //
                    //     // 获取未选中数据
                    //     let notSelectedList = []
                    //
                    //     if (selectionList.length !== 0) notSelectedList = []
                    //
                    //     if (selectionList.length === 0) notSelectedList = hostTableData
                    //
                    //     // 重新赋值对应父级选中数据
                    //     notSelectedList.forEach(notSelected => {
                    //         this.hostSelectedData[currentNodeData.parent.name] = this.hostSelectedData[currentNodeData.parent.name].filter(host => {
                    //             return host['bk_host_innerip'] !== notSelected['bk_host_innerip']
                    //         })
                    //     })
                    //
                    //     if (notSelectedList.length === 0) {
                    //         this.hostSelectedData[currentNodeData.parent.name] = this.hostSelectedData[currentNodeData.parent.name].concat(selectionList)
                    //     }
                    // }
                })
            },

            // 设置选中数据回填
            setHostSelected (params = {}) {
                // let parentName = ''
                // if (params) {
                //     const { name } = params
                //     parentName = name
                // }

                const { hostSelectedData, hostTableData, topTopoName } = this

                // if (!hostSelectedData[activeTopoName]) this.hostSelectedData[activeTopoName] = []

                hostTableData.forEach(row => {
                    const checked = hostSelectedData[topTopoName].some(
                        checkedHost => checkedHost['bk_host_innerip'] === row['bk_host_innerip']
                    )

                    if (checked) this.$refs.multipleTableSelect.toggleRowSelection(row, checked)
                })
                // const { keys } = Object
                // keys(hostSelectedData).forEach(k => {
                //     if (k === activeTopoName) {
                //         hostTableData.forEach(row => {
                //             let resultList = hostSelectedData[k]
                //             // if (parentName) {
                //             //     if (!hostSelectedData[parentName]) this.hostSelectedData[parentName] = []
                //             //     resultList = hostSelectedData[parentName]
                //             // }
                //             if (parentName) resultList = hostSelectedData[parentName]
                //
                //             if (!resultList) return
                //
                //             const checked = resultList.some(
                //                 checkedHost => checkedHost['bk_host_innerip'] === row['bk_host_innerip']
                //             )
                //             if (checked) this.$refs.multipleTableSelect.toggleRowSelection(row, checked)
                //         })
                //     }
                // })
            },

            // 添加主机
            handleConfirm () {
                const { hostSelectedData, treeList, topTopoName } = this
                let results = []
                // if (treeList.length !== 0) results = hostSelectedData[treeList[0].name]
                if (treeList.length !== 0) {
                    results = this.handleUniqueObject(hostSelectedData[topTopoName], 'bk_host_innerip')
                }

                this.$parent.handleGetHostsResult(results)

                const updateConfig = {
                    isShow: false,
                    type: 'confirm'
                }
                this.handleUpdateDialogVisible(updateConfig)
            },

            handleUpdateDialogVisible (params = {}) {
                const { isShow, type } = params
                this.dialogVisible = isShow

                if (!isShow) {
                    this.treeList = []
                    this.hostTableData = []
                    this.handleUpdateActiveTopoName()
                    this.hostSelectedData = {}
                }

                if (type === 'cancel') {
                    this.$parent.handleClearOriginalResult()
                }
            },

            handleUpdateActiveTopoName (value = '') {
                this.activeTopoName = value
            },

            // 防抖函数
            throttle (func, delay) {
                const context = this
                const args = arguments
                if (!context.timer) {
                    context.timer = setTimeout(function () {
                        func.apply(context, args)
                        context.timer = null
                    }, delay)
                }
            },

            handleUniqueObject (arr, prop) {
                return arr.filter((item, index, self) => {
                    return self.findIndex(el => el[prop] === item[prop]) === index
                })
            }
        }
    }
</script>

<style scoped>
  /deep/.tree-expanded-icon {
    margin: 0 4px 0 0;
  }
</style>

<style lang="postcss">
  .select-server-dialog-container {
    .bk-dialog-tool {
      display: none;
    }

    .bk-dialog-body {
      padding: 0;
      .bk-tab-label-wrapper {
        display: flex;
        .bk-tab-label-list {
          display: flex;
          flex: 1;
          .bk-tab-label-item {
            flex: 1
          }
        }
      }
    }

    .select-server-dialog-box {
      .bk-tab-section {
        padding: 20px 20px 0;
        .bk-tab-content {
          display: flex;
          .topology-data-box {
            flex: 0 0 33%;
            height: 100%;
            border-right: 1px solid #dcdee5;
            padding-right: 20px;
            .search-div {
              display: flex;
              margin-bottom: 10px;
            }
            .tree-box {
              height: 456px;
              margin-bottom: 20px;
              overflow: hidden;
              overflow-y: scroll;
            }
            .tree-box::-webkit-scrollbar {
              display: none;
            }
          }

          .host-list-box {
            -webkit-box-flex: 2;
            -ms-flex: 2;
            flex: 2;
            padding-left: 20px;
            /* padding: 0 24px; */
          }
        }
      }
    }

    .bk-dialog-footer {
      border-top: none;
    }
  }
</style>
