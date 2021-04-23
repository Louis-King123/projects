<template>
  <!-- 容器 -->
  <div class="quotaListContainer">
    <!-- 表单-->
    <div class="quotaFormContent">
      <bk-form form-type="inline">

        <bk-form-item label="巡检对象名">
          <bk-input
            style="width: 200px;"
            @keyup.enter.native="handleSearch"
            v-model="searchForm['os_name']">
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
      <div class="addQuotaBtn f12" @click="handleAddOs">
        + 新增巡检对象
      </div>
      <!-- /新增按钮 -->

      <div class="mt30">
        <bk-table
          :data="osList"
          :size="size"
          :pagination="pagination"
          v-bkloading="{ isLoading: isLoading, zIndex: 10 }"
          @page-change="handlePageChange"
          @page-limit-change="handlePageLimitChange">
          <bk-table-column label="巡检对象名" prop="os_name"></bk-table-column>
          <bk-table-column label="创建时间" prop="created_time"></bk-table-column>
          <bk-table-column label="更新时间" prop="updated_time"> </bk-table-column>
          <bk-table-column label="操作" width="180">
            <template slot-scope="scope">
              <bk-button theme="primary" size="small" @click="handleEditOs(scope.row)">编辑</bk-button>
              <bk-button theme="danger" size="small" @click="handleDelOs(scope.row)">删除</bk-button>
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
          <bk-form :label-width="120" :model="osForm" :rules="rules" ref="validateForm">
            <bk-form-item :error-display-type="'normal'" label="巡检对象名" :required="true" :property="'os_name'">
              <bk-input v-model="osForm.os_name"></bk-input>
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
    export default {
        name: 'osList',
        data () {
            return {
                searchForm: {
                    os_name: ''
                },
                osList: [],
                isAdd: true,
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10,
                    limitList: [5, 10, 20]
                },
                size: 'small',
                isLoading: false,
                osId: null,
                isShow: false,
                dialogTitle: '',
                osForm: {
                    os_name: ''
                },
                rules: {
                    os_name: [
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
                    ]
                },
                isFinished: false
            }
        },
        watch: {
            'isShow': {
                handler (newVal) {
                    if (!newVal) {
                        this.clearOsForm()
                    }
                },
                deep: true,
                immediate: true
            }
        },
        created () {
            this.handleSearch()
        },
        methods: {
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

                this.fetch_inspection_os(copyFormData)
            },

            async fetch_inspection_os (param = {}) {
                try {
                    this.isLoading = true

                    const { current, limit } = this.pagination
                    const params = {
                        current,
                        limit,
                        ...param
                    }

                    const res = await this.$store.dispatch('fetch_inspection_os', params)
                    const { data, code } = res
                    if (code === 0) {
                        // this.osList = data.data
                        // this.pagination.count = data.count
                        this.osList = data.data.filter(item => item['is_deleted'] === 0)
                        this.pagination.count = this.osList.length
                    }
                } catch (e) {
                    console.log(e, 'fetch_inspection_os')
                } finally {
                    this.isLoading = false
                }
            },

            handleAddOs () {
                this.handleSetDialogConfig()
            },
            handleEditOs (param) {
                const { id, os_name } = param
                this.osId = id

                const params = {
                    os_name
                }
                const { assign } = Object
                this.osForm = assign(this.osForm, params)

                this.handleSetDialogConfig('edit')
            },

            handleDelOs (param = {}) {
                const { id, os_name } = param
                const params = {
                    os_id: id,
                    is_deleted: 1,
                    os_name
                }

                const okText = '确认删除'
                const theme = 'danger'
                const title = '是否确认删除？'

                this.$bkInfo({
                    theme,
                    title,
                    okText,
                    confirmLoading: true,
                    confirmFn: async () => {
                        this.update_inspection_os(params)
                    }
                })
            },

            handleSubmit () {
                this.$refs.validateForm.validate().then(async () => {
                    const { osForm, isAdd, osId } = this
                    const copyFormData = JSON.parse(JSON.stringify(osForm))

                    if (!isAdd) copyFormData['os_id'] = osId
                    const params = {
                        ...copyFormData
                    }

                    this.update_inspection_os(params)
                }, validator => {
                    return false
                })
            },

            async update_inspection_os (params = {}) {
                try {
                    this.isFinished = true
                    const res = await this.$store.dispatch('update_inspection_os', params)
                    const { code, message } = res
                    const theme = code === 0 ? 'success' : 'error'
                    await this.$bkMessage({ delay: 2000, message, theme })

                    if (code === 0) {
                        this.handleCancel()
                        this.handleSearch()
                    }
                } catch (e) {
                    console.log('update_inspection_os=', e)
                } finally {
                    this.isFinished = false
                }
            },

            handleSetDialogConfig (type = 'add') {
                this.isAdd = true
                this.dialogTitle = '新增巡检对象'

                if (type === 'edit') {
                    this.isAdd = false
                    this.dialogTitle = '编辑巡检对象'
                }

                this.isShow = true
            },
            handleCancel () {
                this.isShow = false
            },
            clearOsForm () {
                const { keys } = Object

                keys(this.osForm).forEach(k => {
                    this.osForm[k] = ''
                })
            }
        }
    }
</script>

<style scoped>
  @import './quotaList.css';
</style>
