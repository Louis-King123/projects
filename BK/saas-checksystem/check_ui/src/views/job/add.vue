<template>
    <div class="addJobContainer">
        <div class="p30">
            <bk-steps
                :ext-cls="stepsConfig.customIcon"
                :steps="stepsConfig.steps"
                :line-type="stepsConfig.lineType"
                :cur-step.sync="stepsConfig.curStep">
            </bk-steps>
        </div>

        <div class="ComStepContainer firstStepContainer" v-show="stepsConfig.curStep === 1">
            <h4 class="mt0">巡检对象</h4>

            <bk-container :col="12">
              <bk-row>
                <bk-col
                  :span="$store.getters.getOsColSpan"
                  v-for="items in $store.getters.getOsList"
                  :key="items.id">
                  <div
                    class="firstStepItem"
                    :class="{ 'active': items.id === taskOs && !isAdd }"
                    @click="handleFirstSelect(items)">
                    <img
                      class="mr20"
                      :src="`${$store.getters.getImgFilePath}${items['os_name'].split('/')[items['os_name'].split('/').length - 1]}.bmp`"
                      alt="">
                    <div>{{ items['os_name'] }}</div>
                  </div>
                </bk-col>
              </bk-row>
            </bk-container>

            <div class="comBtnContainer mt20" v-show="!isAdd">
              <bk-button :theme="'primary'" @click="handleCreate">下一步</bk-button>
            </div>
        </div>

        <div class="ComStepContainer secondStepContainer" v-show="stepsConfig.curStep === 2">
            <h4 class="mt0">选择模板</h4>

            <bk-container :col="12">
              <bk-row>
                <bk-col
                  :span="$store.getters.getTplColSpan"
                  v-for="v in modList"
                  :key="v.id">
                  <div
                    class="secondStepItem"
                    :class="{ 'active': taskTplId === v.id && !isAdd }"
                    @click="handleSecondSelect(v)">
                    <div class="secondStepItemImgContainer">
                      <img
                        :src="`${$store.getters.getImgFilePath}${v['tpl_os_name'].split('/')[v['tpl_os_name'].split('/').length - 1]}.png`"
                        alt=""
                      >
                    </div>

                    <div class="secondStepItemContent">
                      <div>
                        <h5 class="m0 tplNameContainer" v-bk-tooltips.top-start="v['tpl_name']">
                          {{ v['tpl_name'] }}
                        </h5>

                        <div class="fontStyle mt5">
                          <bk-popover :placement="'top-start'" width="230">
                            <div class="descriptionContainer">{{ v.description }}</div>
                            <div slot="content" style="word-break: break-all;">
                              {{ v.description }}
                            </div>
                          </bk-popover>
                        </div>
                      </div>

                      <div class="flexBox" style="justify-content: space-between">
                        <div class="fontStyle">{{ v['created_time'] }}</div>
                        <div class="fontStyle">{{ v.author }}</div>
                      </div>
                    </div>
                  </div>
                </bk-col>
              </bk-row>
            </bk-container>

            <div class="comBtnContainer mt20">
              <bk-button class="mr10" v-show="!isAdd" :theme="'primary'" @click="handleSecond">下一步</bk-button>
              <bk-button :theme="'default'" @click="handleBackStep('1')">
                上一步
              </bk-button>
            </div>
        </div>

        <div class="lastStepContainer" v-show="stepsConfig.curStep === 3">
            <h4 class="mt0 lastStepTitle">创建任务</h4>
            <div class="lastStepContent">
                <bk-form :label-width="100" :model="formData" ref="validateForm" :rules="rules">
                    <bk-form-item :error-display-type="'normal'" label="任务名称" :required="true" :property="'task_name'">
                        <bk-input v-model="formData.task_name"></bk-input>
                    </bk-form-item>

                    <!--目前需求 隐藏-->
                    <!--<bk-form-item label="执行账户" :required="true" :property="'exec_acc'">
                        <bk-input v-model="formData.exec_acc"></bk-input>
                    </bk-form-item>-->

                    <bk-form-item :error-display-type="'normal'" label="选择通知人" :required="true" :property="'notify_usernames'">
                        <bk-select multiple searchable v-model="formData.notify_usernames">
                            <bk-option
                                    v-for="user in userList"
                                    :key="user['username']"
                                    :id="user['username']"
                                    :name="user['display_name'] + '（' + user['username'] + '）'">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>

                    <bk-form-item :error-display-type="'normal'" label="选择业务" :required="true" :property="'biz_id'">
                        <bk-select v-model="formData.biz_id" @change="handleChangeBiz">
                            <bk-option
                              v-for="biz in bizList"
                              :key="biz['bk_biz_id']"
                              :id="biz['bk_biz_id']"
                              :name="biz['bk_biz_name']">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>

                    <bk-form-item :error-display-type="'normal'" label="选择主机" :required="true" :property="'exec_hosts'">
                        <!--<bk-select multiple v-model="formData.exec_hosts">
                            <bk-option
                              v-for="host in hostList"
                              :key="host.id"
                              :id="host.id"
                              :name="host.id">
                            </bk-option>
                        </bk-select>-->
                        <bk-button :theme="'default'" @click="handleAddServer">添加服务器</bk-button>
                        <div class="mt10" v-show="formData.exec_hosts.length > 0">
                          <bk-table :size="'small'" :data="formData.exec_hosts">
                            <bk-table-column label="主机IP" prop="bk_host_innerip"></bk-table-column>
                            <bk-table-column label="云区域" prop="bk_cloud_id"></bk-table-column>
                            <bk-table-column label="主机名" prop="bk_host_name"></bk-table-column>
                            <bk-table-column label="操作系统" prop="bk_os_name"></bk-table-column>
                          </bk-table>
                        </div>
                    </bk-form-item>

                    <bk-form-item :error-display-type="'normal'" label="执行方式" :required="true" :property="'exec_schedule'">
                        <bk-radio-group v-model="formData.exec_schedule" @change="handleChangeExecSchedule">
                            <bk-radio :value="'instant'">单次</bk-radio>
                            <bk-radio :value="'interval'">定时</bk-radio>
                            <bk-radio :value="'crontab'">周期</bk-radio>
                        </bk-radio-group>
                    </bk-form-item>

                    <bk-form-item
                      v-show="formData.exec_schedule !== 'instant'"
                      label="执行时间"
                      :required="true"
                      :error-display-type="'normal'"
                      :property="'exec_start_time'">
                        <bk-date-picker
                          @change="execStartTime"
                          :editable="false"
                          v-model="formData.exec_start_time"
                          :placeholder="'选择日期时间'"
                          :type="'datetime'">
                        </bk-date-picker>
                    </bk-form-item>

                    <bk-form-item
                      v-show="formData.exec_schedule === 'crontab'"
                      label="频率"
                      :error-display-type="'normal'"
                      :required="true"
                      :property="'exec_timec'">
                        <bk-input v-model="formData.exec_timec">
                            <template slot="append">
                                <div class="group-text">天/次</div>
                            </template>
                        </bk-input>
                    </bk-form-item>

                    <bk-form-item>
                        <bk-button
                          v-if="formData.exec_schedule === 'instant'"
                          theme="primary"
                          :loading="isChecking"
                          @click.stop.prevent="handleSubmit('execute')">
                          创建并执行
                        </bk-button>
                        <bk-button
                          v-else
                          theme="primary"
                          :loading="isChecking"
                          @click.stop.prevent="handleSubmit('create')">
                          创建
                        </bk-button>
                        <bk-button v-if="isAdd" :theme="'default'" @click="handleBackStep('2')">上一步</bk-button>
                    </bk-form-item>
                </bk-form>
            </div>

        </div>

        <app-select-server ref="appSelectServer"></app-select-server>
    </div>

</template>

<script>
    export default {
        name: 'add',

        data () {
            return {
                isAdd: true,
                modList: [],
                stepsConfig: {
                    customIcon: 'custom-icon',
                    steps: [
                        {
                            title: '选择巡检对象',
                            icon: 1
                        },
                        {
                            title: '选择模板',
                            icon: 2
                        },
                        {
                            title: '创建任务',
                            icon: 3
                        }
                    ],
                    lineType: 'solid',
                    curStep: 1
                },
                taskOs: null,
                taskTplId: null,
                bizList: [],
                userInfoList: [],
                hostList: [],
                isChecking: false,
                formData: {
                    task_name: '',
                    exec_acc: 'root',
                    biz_id: null,
                    notify_usernames: [],
                    exec_hosts: [],
                    exec_schedule: 'instant',
                    exec_start_time: new Date(),
                    exec_timec: 1
                },
                rules: {
                    task_name: [
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
                    notify_usernames: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    exec_acc: [
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
                    biz_id: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    exec_hosts: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    exec_schedule: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    exec_start_time: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: function () {
                                return true
                            },
                            message: '不可早于当前系统时间',
                            trigger: 'blur'
                        }
                    ],
                    exec_timec: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: function (val) {
                                const { isInteger } = Number
                                return isInteger(Number(val)) && Number(val) > 0
                            },
                            message: '需为大于0的整数',
                            trigger: 'blur'
                        }
                    ]
                },
                editId: null,
                originalHostsResult: []
            }
        },

        async created () {
            this.fetch_business_list()
            this.fetch_user_list()

            // 编辑任务逻辑
            // const { taskId } = this.$route.query
            // if (taskId) {
            //     this.isAdd = false
            //     this.getTask(taskId)
            // }

            // 模板创建任务逻辑
            const { osId, tplId } = this.$route.query
            if (osId) {
                this.stepsConfig.curStep = 3
                this.isAdd = false
                this.taskOs = osId
                this.taskTplId = tplId
            }
        },

        methods: {
            handleAddServer () {
                const { formData, taskOs } = this

                const messageCof = {
                    message: '请先选择业务',
                    theme: 'warning',
                    delay: 3000
                }
                if (!formData['biz_id']) return this.$bkMessage(messageCof)

                const params = {
                    id: formData['biz_id'],
                    osId: taskOs
                }
                this.$refs.appSelectServer.opDialogPop(params)
            },

            handleGetHostsResult (hostResult) {
                this.formData['exec_hosts'] = hostResult

                this.originalHostsResult = hostResult
            },

            handleReturnOriginalResult () {
                const { originalHostsResult } = this
                return originalHostsResult
            },
            handleClearOriginalResult () {
                const { formData } = this
                if (formData['exec_hosts'].length === 0) this.originalHostsResult = []
            },

            handleBackStep (type = '1') {
                if (type === '2') {
                    this.setStepsConfigCur(2)
                    return false
                }

                this.setStepsConfigCur(1)
            },

            execStartTime (date) {
                // this.formData.exec_start_time = date
            },

            // 获取任务详情
            async getTask (taskId) {
                const params = {
                    id: taskId
                }
                const res = await this.$store.dispatch('get_task', params)
                const { data } = res
                const {
                    exec_biz_id, task_name, exec_schedule, id,
                    exec_acc, exec_hosts, exec_start_time, exec_timece, notify_usernames
                } = data

                // 赋值巡检对象ID，模板ID，任务ID
                this.taskOs = data['task_os']
                this.taskTplId = data['task_tpl']
                this.editId = id

                // 回填表单数据
                this.formData = {
                    task_name,
                    exec_acc,
                    exec_schedule,
                    exec_start_time,
                    exec_timec: exec_timece,
                    biz_id: exec_biz_id,
                    notify_usernames: notify_usernames,
                    exec_hosts: exec_hosts.split(',')
                }

                // 编辑任务时初始化判断执行时间是否需要开启
                if (this.formData.exec_schedule !== 'instant') {
                    this.openExecStartTimeValidator()
                }
            },

            // 巡检对象列表卡片点击事件
            async handleFirstSelect (data) {
                const { id } = data
                this.taskOs = id

                await this.fetch_tpl_list()

                const { isAdd } = this
                if (!isAdd) return

                this.setStepsConfigCur(2)
            },
            async handleCreate () {
                await this.fetch_tpl_list()

                this.setStepsConfigCur(2)
            },

            // 模板列表卡片点击事件
            handleSecondSelect (data) {
                const { id } = data
                this.taskTplId = id

                const { isAdd } = this
                if (!isAdd) return

                this.setStepsConfigCur(3)
            },
            handleSecond () {
                this.setStepsConfigCur(3)
            },

            // 获取模板列表
            async fetch_tpl_list () {
                try {
                    const { taskOs } = this
                    const params = {
                        os_id: taskOs
                    }
                    const res = await this.$store.dispatch('fetch_tpl_list', params)

                    const { data } = res
                    this.modList = data
                } catch (e) {

                }
            },

            async fetch_business_list () {
                try {
                    const res = await this.$store.dispatch('fetch_business_list')
                    const { data } = res
                    this.bizList = data
                } catch (e) {

                }
            },
            async fetch_user_list () {
                try {
                    const res = await this.$store.dispatch('fetch_user_list')
                    const { data } = res
                    this.userList = data
                } catch (e) {

                }
            },
            handleChangeBiz (value) {
                this.formData.biz_id = value

                if (!value) {
                    // this.hostList = []
                    this.formData.exec_hosts = []
                }

                // this.search_host_by_biz(value)
            },
            async search_host_by_biz (k) {
                try {
                    const res = await this.$store.dispatch('search_host_by_biz')

                    const { data } = res
                    this.hostList = data[k].children
                } catch (e) {

                }
            },

            // 根据单选框的值重新赋值执行时间和频率的值
            handleChangeExecSchedule (value) {
                if (value !== 'crontab') this.formData.exec_timec = 1

                if (value !== 'instant') this.openExecStartTimeValidator()

                if (value === 'instant') {
                    this.formData.exec_start_time = new Date()

                    this.closeExecStartTimeValidator()
                }
            },
            // 屏蔽执行时间是否早于当前时间的判断
            closeExecStartTimeValidator () {
                this.rules.exec_start_time[1].validator = () => true
            },
            // 开启执行时间是否早于当前时间的判断
            openExecStartTimeValidator () {
                this.rules.exec_start_time[1].validator = val => val.getTime() >= Date.now()
            },

            // 创建
            handleSubmit (type = 'create') {
                this.$refs.validateForm.validate().then(async () => {
                    try {
                        this.isChecking = true
                        const { taskTplId, taskOs, formData } = this

                        const copyFormData = JSON.parse(JSON.stringify(formData))
                        const execAcc = this.handleSetExecAcc(taskOs)
                        copyFormData['exec_start_time'] = this.$moment(copyFormData['exec_start_time']).format('YYYY-MM-DD HH:mm:ss')
                        copyFormData['exec_acc'] = execAcc

                        const params = {
                            task_tpl_id: taskTplId,
                            task_os: taskOs,
                            ...copyFormData
                        }

                        // 编辑情况时组装任务ID参数
                        // const { editId, isAdd } = this
                        // if (!isAdd) data['task_id'] = editId

                        const res = await this.$store.dispatch('task_add', params)

                        const { code, message, data } = res
                        const theme = code === 0 ? 'success' : 'error'

                        if (code !== 0) {
                            return this.$bkMessage({ delay: 3000, message, theme })
                        }

                        // 执行逻辑
                        if (type === 'execute') {
                            const executeParams = {
                                task_id: data[0].id
                            }
                            const executeRes = await this.$store.dispatch('execute_task', executeParams)
                            const { code, message } = executeRes
                            const theme = code === 0 ? 'success' : 'error'

                            if (code !== 0) {
                                return this.$bkMessage({ delay: 3000, message, theme })
                            }
                        }

                        const h = this.$createElement
                        const tipDom = this.$bkInfo({
                            type: theme,
                            title: message,
                            showFooter: false,
                            subHeader: h('div', [
                                h('bk-button', {
                                    props: {
                                        theme: 'primary',
                                        plain: true
                                    },
                                    on: {
                                        click: () => {
                                            this.$router.push({
                                                name: 'jobList'
                                            })
                                            setTimeout(() => tipDom.close())
                                        }
                                    }
                                }, '返回列表')
                            ])
                        })
                    } catch (e) {

                    } finally {
                        this.isChecking = false
                    }
                }, validator => {
                    return false
                })
            },

            setStepsConfigCur (step = 1) {
                this.stepsConfig.curStep = step
            },

            handleSetExecAcc (type = 3) {
                if (type === 3) return 'system'

                return 'root'
            }

        }
    }
</script>

<style lang="postcss" scoped>
    .flexBox {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
    }
    .fontStyle {
      font-size: 12px;
      color: #ccc;
    }

    .active {
      background: #1d91ec !important;
    }

    .bk-form-radio {
        margin-right: 30px;
    }

    .addJobContainer {
        width: 100%;
        height: 100%;
    }

    .ComStepContainer {
        padding: 20px;
        background: #F5F5F5;
    }
    .ComStepContent {
      display: flex;
      flex-wrap: wrap;
    }
    .comBtnContainer {
      display: flex;
      justify-content: flex-end;
    }

    .firstStepContainer {
      background: #ffffff;
      margin: 0 20px;
    }
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

    .secondStepContainer {
      margin: 0 20px;
      background-color: #fff;
    }
    .secondStepContent {
      width: 100%;
      height: 100%;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
    }
    .secondStepItem {
      width: 250px;
      height: 260px;
      border: 1px solid #ccc;
      background: #FFFFFF;
      box-shadow: 4px 4px 6px #ccc;
      cursor: pointer;
      margin: 0 auto 20px auto;
    }
    .secondStepItemImgContainer {
      height: 60%;
      width: 100%;
    }
    .secondStepItemImgContainer img {
      width: 100%;
      height: 100%;
    }
    .secondStepItemContent {
      width: 100%;
      height: 40%;
      padding: 10px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;

    }
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

    .lastStepContainer {
      width: 600px;
      margin: 0 auto;
      padding: 20px;
      background: #ffffff;
    }
    .lastStepTitle {
      width: 100px;
      text-align: right;
      padding-right: 24px;
    }

</style>
