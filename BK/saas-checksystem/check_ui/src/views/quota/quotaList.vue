<template>
  <!-- 容器 -->
  <div class="quotaListContainer">
    <!-- 表单-->
    <div class="quotaFormContent">
      <bk-form form-type="inline">
        <bk-form-item label="巡检对象">
          <bk-select style="width: 200px;" v-model="searchForm.quota_os">
            <bk-option v-for="os in $store.getters.getOsList" :key="os.id" :id="os.id" :name="os['os_name']">
            </bk-option>
          </bk-select>
        </bk-form-item>

        <bk-form-item label="巡检项名称">
          <bk-input style="width: 200px;" @keyup.enter.native="handleSearch" v-model="searchForm.quota_name">
          </bk-input>
        </bk-form-item>

        <bk-form-item>
          <bk-button ext-cls="mr5" theme="primary" @click="handleSearch">查询</bk-button>
        </bk-form-item>
      </bk-form>
    </div>
    <!-- /表单-->

    <!-- 表格 -->
    <div class="quotaListTableContent">
      <!-- 新增按钮 -->
      <div class="addQuotaBtn f12" @click="handleAddQuota">
        + 新增指标
      </div>
      <!-- /新增按钮 -->

      <div class="mt30">
        <bk-table
          :data="quotaList"
          :size="size"
          :pagination="pagination"
          v-bkloading="{ isLoading: isLoading, zIndex: 10 }"
          @page-change="handlePageChange"
          @page-limit-change="handlePageLimitChange">
          <bk-table-column
            label="巡检项名称"
            prop="quota_name"
            width="100"
            :show-overflow-tooltip="true">
          </bk-table-column>
          <bk-table-column label="巡检对象" prop="quota_os"></bk-table-column>
          <bk-table-column label="对比方式">
            <template slot-scope="scope">
              <span>{{ setQuotaHandler(scope.row['quota_handler']) }}</span>
            </template>
          </bk-table-column>
          <bk-table-column label="对比值" prop="quota_threshold"></bk-table-column>
          <bk-table-column label="脚本类型">
            <template slot-scope="scope">
              <span>{{ setScriptType(scope.row['script_type']) }}</span>
            </template>
          </bk-table-column>
          <bk-table-column
            label="脚本"
            prop="script_content"
            :show-overflow-tooltip="true">
          </bk-table-column>
          <bk-table-column label="操作" width="180">
            <template slot-scope="scope">
              <bk-button theme="primary" size="small" @click="handleEdit(scope.row)">编辑</bk-button>
              <bk-button theme="danger" size="small" @click="handleDel(scope.row)">删除</bk-button>
            </template>
          </bk-table-column>
        </bk-table>
      </div>
    </div>
    <!-- /表格 -->

    <!-- 右侧栏 -->
    <div>
      <bk-sideslider :is-show.sync="isShow" :title="dialogTitle" :quick-close="true" width="700">
        <div slot="content" class="dialogContent">
          <bk-form :label-width="120" :model="quotaForm" :rules="rules" ref="validateForm">
            <bk-form-item :error-display-type="'normal'" label="巡检项名称" :required="true" :property="'quota_name'">
              <bk-input v-model="quotaForm.quota_name" :disabled="!isAdd"></bk-input>
            </bk-form-item>

            <bk-form-item :error-display-type="'normal'" label="巡检对象" :required="true" :property="'quota_os'">
              <bk-select v-model="quotaForm.quota_os" :disabled="!isAdd">
                <bk-option
                  v-for="os in $store.getters.getOsList"
                  :key="os.id"
                  :id="os.id"
                  :name="os['os_name']">
                </bk-option>
              </bk-select>
            </bk-form-item>

            <bk-form-item :error-display-type="'normal'" label="脚本类型" :required="true" :property="'script_type'">
              <bk-select v-model="quotaForm.script_type">
                <bk-option
                  v-for="script in scriptTypes"
                  :key="script.id"
                  :id="script.id"
                  :name="script.name">
                </bk-option>
              </bk-select>
            </bk-form-item>

            <bk-form-item :error-display-type="'normal'" label="脚本内容" :required="true" :property="'script_content'">
              <bk-input :type="'textarea'" :rows="5" v-model="quotaForm.script_content"></bk-input>
            </bk-form-item>

            <bk-form-item label="是否设置对比">
              <bk-switcher
                v-model="quotaForm.isSetHandler"
                theme="primary"
                :show-text="true"
                :on-text="'是'"
                :off-text="'否'"
              ></bk-switcher>
            </bk-form-item>

            <bk-form-item label="对比方式" :property="'quota_handler'">
              <bk-select
                v-model="quotaForm.quota_handler"
                :disabled="!quotaForm.isSetHandler"
                @change="handleChangeQuotaHandler">
                <bk-option v-for="h in handlers" :key="h.val" :id="h.val" :name="h.name"></bk-option>
              </bk-select>
            </bk-form-item>

            <bk-form-item label="对比值" :property="'quota_threshold'">
              <bk-input
                :placeholder="' '"
                v-model="quotaForm.quota_threshold"
                :disabled="!quotaForm.isSetHandler">
              </bk-input>
            </bk-form-item>

            <bk-form-item>
              <bk-button ext-cls="mr5" theme="primary" :loading="isFinished" @click="handleSubmit">提交</bk-button>
              <bk-button theme="default" @click="handleCancel">取消</bk-button>
            </bk-form-item>
          </bk-form>
        </div>
      </bk-sideslider>
    </div>
    <!-- /右侧栏 -->

  </div>
  <!-- /容器 -->
</template>

<script>
    import { mapGetters } from 'vuex'

    export default {
        name: 'quotaList',
        data () {
            return {
                searchForm: {
                    quota_os: '',
                    quota_name: ''
                },
                isAdd: true,
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10,
                    limitList: [5, 10, 20]
                },
                size: 'small',
                isLoading: false,
                quotaList: [],
                quotaId: null,
                scriptTypes: [
                    {
                        id: 1,
                        name: 'shell脚本'
                    },
                    {
                        id: 2,
                        name: 'bat脚本'
                    },
                    {
                        id: 3,
                        name: 'perl脚本'
                    },
                    {
                        id: 4,
                        name: 'python脚本'
                    },
                    {
                        id: 5,
                        name: 'powerShell脚本'
                    }
                ],
                handlers: [
                    {
                        name: '>',
                        val: 'cmp_integer_gt'
                    },
                    {
                        name: '>=',
                        val: 'cmp_integer_gte'
                    },
                    {
                        name: '<',
                        val: 'cmp_integer_lt'
                    },
                    {
                        name: '<=',
                        val: 'cmp_integer_lte'
                    },
                    {
                        name: '==',
                        val: 'cmp_string_eq'
                    },
                    {
                        name: '!=',
                        val: 'cmp_string_neq'
                    }
                ],
                isShow: false,
                dialogTitle: '',
                quotaForm: {
                    quota_name: '',
                    quota_os: '',
                    script_type: '',
                    script_content: '',
                    isSetHandler: false,
                    quota_handler: '',
                    quota_threshold: ''
                },
                rules: {
                    quota_name: [
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
                    quota_os: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    script_type: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    script_content: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    quota_handler: [
                        {
                            required: false,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    quota_threshold: [
                        {
                            required: false,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: function () {
                                return true
                            },
                            message: '在对比方式为“>”“>=”“<”“<=”时仅可输入正数(包含整型和浮点型)',
                            trigger: 'blur'
                        },
                        {
                            max: 8,
                            message: '不能多于8个字符',
                            trigger: 'blur'
                        }
                    ]
                },
                isFinished: false
            }
        },
        watch: {
            isShow (newVal) {
                if (!newVal) {
                    this.clearQuotaForm()
                }
            },

            // 用户设置对比方式时 对比方式和对比值不能为空 否则可为空
            'quotaForm.isSetHandler': {
                deep: true,
                handler (val) {
                    this.rules.quota_handler[0].required = val
                    this.rules.quota_threshold[0].required = val

                    if (!val) {
                        this.$refs.validateForm.clearError()

                        this.closeQuotaThresholdValidator()
                    }
                }
            }
        },
        created () {
            this.handleSearch()
        },
        methods: {
            ...mapGetters(['getUsername']),

            handleChangeQuotaHandler (value) {
                if (value === 'cmp_string_eq' || value === 'cmp_string_neq') {
                    this.closeQuotaThresholdValidator()
                    return false
                }

                this.openQuotaThresholdValidator()
            },
            // 屏蔽对比值校验
            closeQuotaThresholdValidator () {
                this.rules.quota_threshold[1].validator = () => true
            },
            // 开启对比值校验
            openQuotaThresholdValidator () {
                this.rules.quota_threshold[1].validator = val => {
                    const { isFinite } = Number
                    return isFinite(Number(val)) && Number(val) > 0
                }
            },

            handlePageChange (current) {
                this.pagination.current = current
                this.handleSearch()
            },
            handlePageLimitChange (limit) {
                this.pagination.current = 1
                this.pagination.limit = limit
                this.handleSearch()
            },
            handleSearch () {
                const { searchForm } = this
                const copyFormData = JSON.parse(JSON.stringify(searchForm))

                const { keys } = Object
                keys(copyFormData).forEach(k => {
                    if (!copyFormData[k]) {
                        delete copyFormData[k]
                    }
                })

                copyFormData['author'] = this.getUsername()
                console.log(this.getUsername(), '-------------------')

                this.fetch_custom_quota(copyFormData)
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
            // 设置脚本类型展示
            setScriptType (type) {
                if (!type) return
                if (type === 1) return 'shell脚本'
                if (type === 2) return 'bat脚本'
                if (type === 3) return 'perl脚本'
                if (type === 4) return 'python脚本'
                if (type === 5) return 'powerShell脚本'
            },

            async fetch_custom_quota (param = {}) {
                const customize = {
                    ...param
                }

                const { current, limit } = this.pagination
                const params = {
                    current,
                    limit,
                    customize: JSON.stringify(customize)
                }

                try {
                    this.isLoading = true
                    const res = await this.$store.dispatch('fetch_custom_quota', params)
                    const { code } = res
                    if (code !== 0) return

                    const { data } = res
                    this.quotaList = data.data
                    this.pagination.count = data.count
                } catch (e) {
                    console.log('fetch_custom_quota=', e)
                } finally {
                    this.isLoading = false
                }
            },

            handleAddQuota () {
                this.setDialogConfig(0)
            },
            handleEdit (param) {
                const { id } = param
                this.quotaId = id

                const { keys } = Object
                keys(param).forEach(k => {
                    if (this.quotaForm.hasOwnProperty(k)) {
                        this.quotaForm[k] = param[k]
                        if (param['quota_threshold'] || param['quota_handler'] !== 'cmp_show') {
                            this.quotaForm.isSetHandler = true
                        }
                        if (k === 'quota_os') this.quotaForm['quota_os'] = +param['quota_os_id']
                        if (k === 'quota_handler' && param['quota_handler'] === 'cmp_show') this.quotaForm[k] = ''
                    }
                })

                if (param['related_tpl'].length > 0) {
                    const tplStr = param['related_tpl'].map(item => `【${item['tpl_name']}】`).join('')
                    const subTitle = `该巡检项目前已被引用于${tplStr}，编辑后上述模板也将变更，是否继续？`

                    return this.$bkInfo({
                        theme: 'warning',
                        title: '确认要编辑？',
                        subTitle,
                        okText: '继续编辑',
                        confirmFn: () => this.setDialogConfig(1)
                    })
                }

                this.setDialogConfig(1)
            },
            setDialogConfig (type = 0) {
                this.isAdd = true
                this.dialogTitle = '新增指标'

                if (type !== 0) {
                    this.isAdd = false
                    this.dialogTitle = '编辑指标'
                }

                this.isShow = true
            },
            handleDel (param = {}) {
                const { id } = param
                const params = {
                    quota_id: id
                }

                let isCanDel = true
                let subTitle = '该巡检项目前未被引用于任何模板，是否确认删除？'
                let okText = '确认删除'
                let theme = 'danger'
                const title = '确认要删除？'

                if (param['related_tpl'].length > 0) {
                    const tplStr = param['related_tpl'].map(item => `【${item['tpl_name']}】`).join('')
                    subTitle = `该巡检项目前已被引用于${tplStr}，不支持删除！`
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
                        if (isCanDel) return this.custom_quota_delete(params)

                        return true
                    }
                })
            },
            async custom_quota_delete (params = {}) {
                try {
                    const res = await this.$store.dispatch('custom_quota_delete', params)
                    const { code, message } = res
                    const theme = code === 0 ? 'success' : 'error'
                    await this.$bkMessage({ delay: 2000, message, theme })

                    if (code === 0) this.handleSearch()
                } catch (e) {
                    console.log('custom_quota_delete=', e)
                }
            },

            handleSubmit () {
                this.$refs.validateForm.validate().then(async () => {
                    const { quotaForm, isAdd, quotaId } = this
                    const copyFormData = JSON.parse(JSON.stringify(quotaForm))

                    const { keys } = Object
                    keys(copyFormData).forEach(k => {
                        // 编辑 不设置对比时 对比方式设置为展示 对比值设置为空字符串
                        if (!copyFormData[k] && k === 'isSetHandler' && !isAdd) {
                            copyFormData['quota_handler'] = 'cmp_show'
                            copyFormData['quota_threshold'] = ''
                        }

                        // 添加逻辑
                        if (!copyFormData[k] && isAdd) delete copyFormData[k]

                        if (k === 'isSetHandler') delete copyFormData[k]
                    })

                    const params = {
                        ...copyFormData
                    }

                    // 编辑逻辑
                    if (!isAdd) {
                        params['quota_id'] = quotaId
                        this.custom_quota_update(params)
                        return
                    }

                    // 新增逻辑
                    params['username'] = this.getUsername()
                    this.custom_quota_add(params)
                }, validator => {
                    return false
                })
            },
            async custom_quota_add (params = {}) {
                try {
                    this.isFinished = true
                    const res = await this.$store.dispatch('custom_quota_add', params)
                    const { code, message } = res
                    const theme = code === 0 ? 'success' : 'error'
                    await this.$bkMessage({ delay: 2000, message, theme })

                    if (code === 0) {
                        this.handleCancel()
                        this.handleSearch()
                    }
                } catch (e) {
                    console.log('custom_quota_add=', e)
                } finally {
                    this.isFinished = false
                }
            },
            async custom_quota_update (params = {}) {
                try {
                    this.isFinished = true
                    const res = await this.$store.dispatch('custom_quota_update', params)
                    const { code, message } = res
                    const theme = code === 0 ? 'success' : 'error'
                    await this.$bkMessage({ delay: 2000, message, theme })

                    if (code === 0) {
                        this.handleCancel()
                        this.handleSearch()
                    }
                } catch (e) {
                    console.log('custom_quota_update=', e)
                } finally {
                    this.isFinished = false
                }
            },
            handleCancel () {
                this.isShow = false
            },
            clearQuotaForm () {
                const { keys } = Object

                keys(this.quotaForm).forEach(k => {
                    this.quotaForm[k] = ''

                    if (k === 'isSetHandler') this.quotaForm[k] = false
                })
            }
        }
    }
</script>

<style scoped>
  @import './quotaList.css';
</style>
