<template>
    <!-- 容器 -->
    <div class="addModuleContainer">
        <!-- 步骤条 -->
        <div class="p30">
            <bk-steps
              :ext-cls="stepsConfig.customIcon"
              :steps="stepsConfig.steps"
              :line-type="stepsConfig.lineType"
              :cur-step.sync="stepsConfig.curStep">
            </bk-steps>
        </div>
        <!-- /步骤条 -->

        <!-- 步骤一内容容器 -->
        <div class="comStepContainer firstStepContainer" v-show="stepsConfig.curStep === 1">
            <!-- 标题 -->
            <h4 class="mt0">巡检对象</h4>
            <!-- /标题 -->

            <!-- content -->
            <bk-container :col="12">
              <bk-row>
                <bk-col :span="$store.getters.getOsColSpan" v-for="v in $store.getters.getOsList" :key="v.id">
                  <div class="firstStepItem" :class="{ 'active': v.id === activeId && !isAdd }" @click="handleFirstSelect(v)">
                    <img class="mr20" alt=""
                      :src="`${$store.getters.getImgFilePath}${v['os_name'].split('/')[v['os_name'].split('/').length - 1]}.bmp`"
                    >
                    <div>{{ v['os_name'] }}</div>
                  </div>
                </bk-col>
              </bk-row>
            </bk-container>
            <!-- /content -->

            <!-- 按钮 -->
            <div class="comBtnContainer mt20" v-show="!isAdd">
                <bk-button :theme="'primary'" :loading="isFinished" @click="handleCreate">下一步</bk-button>
            </div>
            <!-- /按钮 -->
        </div>
        <!-- /步骤一内容容器 -->

        <!-- 步骤二内容容器 -->
        <div class="comStepContainer secondStepContainer" v-show="stepsConfig.curStep === 2">
            <!-- 标题 -->
            <h4 class="mt0">巡检指标</h4>
            <!-- /标题 -->

            <!-- content -->
            <bk-collapse v-model="activeName">
              <div class="secondStepContent pl5">
                <div class="secondStepItem mb20" v-for="v in quotaList" :key="v.id">
                  <bk-collapse-item :name="v['class_name']">
                    <h5 class="m0">{{ v['class_name'] }}</h5>
                    <div slot="content" class="pb10">
                      <bk-table
                        :data="v.children"
                        :ref="`quotaTable${v.id}`"
                        @selection-change="handleSelectQuota"
                        @select-all="setActiveQuota(v)"
                        @select="setActiveQuota(v)">
                        <bk-table-column type="selection" width="60" :selectable="isCanSelect"></bk-table-column>

                        <bk-table-column label="检查项" prop="quota_name"></bk-table-column>

                        <bk-table-column label="对比方式">
                          <template slot-scope="scope">
                            <span>{{ setQuotaHandler(scope.row['quota_handler']) }}</span>
                          </template>
                        </bk-table-column>

                        <bk-table-column label="推荐值">
                          <template slot-scope="scope">
                            <div v-if="scope.row['quota_handler'] !== 'cmp_show'">
                              <bk-input
                                :placeholder="' '"
                                :clearable="true"
                                :maxlength="20"
                                v-model="scope.row['quota_threshold']">
                              </bk-input>
                            </div>
                          </template>
                        </bk-table-column>
                      </bk-table>
                    </div>
                  </bk-collapse-item>
                </div>
              </div>
            </bk-collapse>
            <!-- /content -->

            <!-- 按钮 -->
            <div class="comBtnContainer mt20">
              <bk-button class="mr10" :theme="'primary'" @click="handleSecond">下一步</bk-button>
              <bk-button :theme="'default'" @click="handleBackStep('1')">上一步</bk-button>
            </div>
            <!-- /按钮 -->
        </div>
        <!-- /步骤二内容容器 -->

        <!-- 步骤三内容容器 -->
        <div class="lastStepContainer" v-show="stepsConfig.curStep === 3">
            <!-- 标题 -->
            <h4 class="mt0 lastStepTitle">创建模板</h4>
            <!-- /标题 -->

            <!-- content -->
            <div class="lastStepContent">
                <bk-form :label-width="100" :model="formData" :rules="rules" ref="validateForm">
                    <!-- 模板名 -->
                    <bk-form-item :error-display-type="'normal'" label="模板名称" :required="true" :property="'tpl_name'">
                        <bk-input v-model="formData.tpl_name" placeholder="请输入模板名称"> </bk-input>
                    </bk-form-item>
                    <!-- /模板名 -->

                    <!-- 说明-->
                    <bk-form-item :error-display-type="'normal'" label="说明" :property="'description'">
                      <bk-input :type="'textarea'" :rows="3" v-model="formData.description"></bk-input>
                    </bk-form-item>
                    <!-- /说明 -->

                    <!-- 按钮-->
                    <bk-form-item>
                        <bk-button
                          ext-cls="mr5"
                          theme="primary"
                          @click.stop.prevent="handleSubmit"
                          :loading="isChecking">
                          创建
                        </bk-button>
                        <bk-button :theme="'default'" @click="handleBackStep('2')">上一步</bk-button>
                    </bk-form-item>
                    <!-- /按钮 -->
                </bk-form>
            </div>
            <!-- /content -->
        </div>
        <!-- 步骤三内容容器 -->
    </div>
    <!-- /容器 -->
</template>

<script>
    export default {
        inject: ['reload'],

        name: 'add',

        data () {
            return {
                isAdd: true,
                activeId: null,
                stepsConfig: {
                    customIcon: 'custom-icon',
                    steps: [
                        {
                            title: '选择巡检对象',
                            icon: 1
                        },
                        {
                            title: '选择巡检指标',
                            icon: 2
                        },
                        {
                            title: '创建模板',
                            icon: 3
                        }
                    ],
                    lineType: 'solid',
                    curStep: 1
                },
                quotaList: [],
                quotaData: {},
                activeQuota: '',
                quotaResults: [],
                isChecking: false,
                formData: {
                    tpl_name: '',
                    description: ''
                },
                rules: {
                    tpl_name: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            max: 20,
                            message: '不能多于20个字符',
                            trigger: 'blur'
                        }
                    ],
                    description: [
                        {
                            max: 225,
                            message: '不能多于225个字符',
                            trigger: 'blur'
                        }
                    ]
                },
                tplId: null,
                tplInfo: {},
                activeName: [],
                isFinished: false
            }
        },

        created () {
            // 复制模板逻辑
            const { id, tpl_os } = this.$route.query
            if (id) {
                this.isAdd = false
                this.activeId = Number(tpl_os)
                this.tplId = id

                const params = {
                    tpl_id: id
                }
                this.tpl_info(params)
            }
        },

        methods: {
            // 设置默认选中项不可取消勾选
            isCanSelect (row) {
                return row['is_required'] !== 1
            },

            handleBackStep (type = '1') {
                if (type === '2') {
                    this.stepsConfig.curStep = 2
                    return false
                }
                this.stepsConfig.curStep = 1

                this.reload()
            },

            // 设置对比方式展示
            setQuotaHandler (handler) {
                if (!handler) return
                const handlerList = handler.split('_')
                if (handlerList.includes('eq')) return '=='
                if (handlerList.includes('neq')) return '!='
                if (handlerList.includes('gt')) return '>'
                if (handlerList.includes('gte')) return '>='
                if (handlerList.includes('lt')) return '<'
                if (handlerList.includes('lte')) return '<='
                if (handlerList.includes('disk')) return '磁盘内容'
                if (handlerList.includes('show')) return '展示'
            },
            // 复制模板逻辑
            handleCreate () {
                this.isFinished = true
                this.fetch_os_quota()
                    .then(() => {
                        this.setQuotaChecked()
                        this.stepsConfig.curStep = 2
                    })
                    .finally(() => {
                        this.isFinished = false
                    })
            },
            // 获取模板详情
            async tpl_info (params) {
                try {
                    const res = await this.$store.dispatch('tpl_info', params)
                    const { data } = res
                    this.tplInfo = data
                } catch (e) {
                    console.log('tpl_info=', e)
                }
            },
            // 巡检指标数据回填
            setQuotaChecked () {
                const { quotaList, tplInfo, activeId } = this

                if (tplInfo['tpl_os'] !== String(activeId)) return

                const checkedQuotas = []
                if (tplInfo['tpl_quotas']) {
                    tplInfo['tpl_quotas'].forEach(quota => {
                        quota.children.forEach(quotaItem => {
                            checkedQuotas.push(quotaItem)

                            // 编辑模板情况下初始化巡检指标数据
                            this.quotaData[quotaItem['quota_class_id']].push(quotaItem)
                        })
                    })
                }

                quotaList.forEach(item => {
                    item.children.forEach(row => {
                        const checked = checkedQuotas.some(checkedQuota => checkedQuota.id === row.id)
                        if (checked) {
                            checkedQuotas.forEach(checkedQuota => {
                                if (checkedQuota.id === row.id) row['quota_threshold'] = checkedQuota['quota_threshold']
                            })

                            const refInst = this.$refs[`quotaTable${row['quota_class_id']}`][0]
                            refInst.toggleRowSelection(row, checked)
                        }
                    })
                })
            },

            // operateFirstStep
            handleFirstSelect (param) {
                const { id } = param
                this.activeId = id

                const { isAdd } = this

                if (isAdd) {
                    this.fetch_os_quota()
                        .then(() => {
                            this.stepsConfig.curStep = 2
                        })
                }
            },

            // 获取巡检指标
            async fetch_os_quota () {
                try {
                    const { activeId } = this
                    const params = {
                        id: activeId
                    }
                    const res = await this.$store.dispatch('fetch_os_quota', params)
                    const { data } = res
                    this.quotaList = data

                    if (data) {
                        data.forEach(item => {
                            // 初始化巡检指标数据
                            this.quotaData[item.id] = []

                            // 添加默认选中的数据
                            item.children.forEach(child => {
                                if (child['is_required'] === 1) {
                                    this.quotaData[item.id].push(child)
                                }
                            })

                            // 初始化各大类展开
                            this.activeName.push(item['class_name'])
                        })
                    }

                    // 设置默认选中
                    if (this.quotaList) {
                        this.quotaList.forEach(item => {
                            item.children.forEach(row => {
                                const checked = row['is_required'] === 1
                                if (checked) {
                                    this.$nextTick(() => {
                                        const refInst = this.$refs[`quotaTable${row['quota_class_id']}`][0]
                                        refInst.toggleRowSelection(row, checked)
                                    })
                                }
                            })
                        })
                    }
                } catch (e) {
                    console.log('fetch_os_quota=', e)
                }
            },
            // 选择巡检指标
            handleSelectQuota (selection) {
                this.$nextTick(() => {
                    const { activeQuota } = this
                    if (activeQuota) {
                        this.quotaData[activeQuota] = [...selection]
                    }
                })
            },
            // 保存巡检指标操作项
            setActiveQuota (param) {
                const { id } = param
                this.activeQuota = id
            },
            // operateSecondStep
            handleSecond () {
                this.setQuotaResults()

                const { quotaResults } = this
                if (quotaResults.length === 0) {
                    return this.$bkMessage({
                        message: '请至少选择一项巡检指标！',
                        theme: 'warning',
                        delay: 3000
                    })
                }

                this.stepsConfig.curStep = 3
            },
            // 设置quotas参数
            setQuotaResults () {
                const { quotaList, isAdd } = this
                const { keys } = Object

                this.quotaResults = []

                if (!isAdd) {
                    quotaList.forEach(item => {
                        item.children.forEach(row => {
                            this.quotaData[row['quota_class_id']].forEach(quotaDataItem => {
                                if (quotaDataItem.id === row.id) {
                                    quotaDataItem['quota_threshold'] = row['quota_threshold']
                                }
                            })
                        })
                    })
                }

                keys(this.quotaData).forEach(k => {
                    if (k) {
                        this.quotaData[k].forEach(v => {
                            const ids = v.id.split('-')
                            this.quotaResults.push({
                                id: ids[1],
                                quota_threshold: v.quota_threshold
                            })
                        })
                    }
                })
            },

            // 创建&更新模板
            handleSubmit () {
                this.$refs.validateForm.validate().then(async () => {
                    try {
                        this.isChecking = true
                        // const { activeId, quotaResults, formData, isAdd, tplId } = this
                        const { activeId, quotaResults, formData } = this

                        const params = {
                            tpl_os: activeId,
                            quotas: quotaResults,
                            ...formData
                        }

                        const resultUrl = 'tpl_add'
                        // let resultUrl = 'tpl_add'

                        // 更新模板
                        // if (!isAdd) {
                        //     resultUrl = 'tpl_update'
                        //     data['tpl_id'] = tplId
                        // }

                        const res = await this.$store.dispatch(resultUrl, params)

                        const { code, message, data } = res
                        const theme = code === 0 ? 'success' : 'error'

                        if (code !== 0) {
                            return this.$bkMessage({ delay: 3000, message, theme })
                        }

                        const h = this.$createElement
                        const tipDom = this.$bkInfo({
                            type: theme,
                            title: message,
                            showFooter: false,
                            subHeader: h('div', [
                                h('bk-button', {
                                    class: 'mr5',
                                    props: {
                                        theme: 'primary',
                                        plain: true
                                    },
                                    on: {
                                        click: () => {
                                            this.$router.push({
                                                name: 'moduleList'
                                            })
                                            handleCloseTip()
                                        }
                                    }
                                }, '返回列表'),
                                h('bk-button', {
                                    props: {
                                        theme: 'primary',
                                        plain: true
                                    },
                                    on: {
                                        click: () => {
                                            const { tpl_os, tpl_id } = data
                                            this.$router.push({
                                                name: 'jobAdd',
                                                query: {
                                                    osId: tpl_os,
                                                    tplId: tpl_id
                                                }
                                            })
                                            handleCloseTip()
                                        }
                                    }
                                }, '去创建任务')
                            ])
                        })

                        const handleCloseTip = () => {
                            setTimeout(() => tipDom.close())
                        }
                    } catch (e) {
                        console.log('tpl_add=', e)
                    } finally {
                        this.isChecking = false
                    }
                }, validator => {
                    return false
                })
            }
        }
    }
</script>

<style lang="postcss" scoped>
  .addModuleContainer {
    width: 100%;
    height: 100%;

    .comStepContainer {
      padding: 20px;
      background: #F5F5F5;

      .comBtnContainer {
        display: flex;
        justify-content: flex-end;
      }

      .active {
        background: #1d91ec;
      }
    }

    .firstStepContainer {
      background: #ffffff;
      margin: 0 20px;

      .firstStepItem {
        display: flex;
        align-items: center;
        padding: 0 20px;
        width: 280px;
        height: 100px;
        border: 1px solid #ccc;
        cursor: pointer;
        margin: 0 auto 20px auto;
        font-weight: 600;
      }
    }

    .secondStepContainer {
      margin: 0 20px;

      .secondStepContent {
        width: 100%;
        height: 100%;

        .secondStepItem {
          width: 100%;
          background: #ffffff;
          border-radius: 6px;
        }
      }
    }

    .lastStepContainer {
      width: 600px;
      margin: 0 auto;
      padding: 20px;
      background: #ffffff;

      .lastStepTitle {
        width: 100px;
        text-align: right;
        padding-right: 24px;
      }
    }
  }
</style>
