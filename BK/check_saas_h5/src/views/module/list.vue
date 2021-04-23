<template>
    <div style="margin-top: 20px;">
        <bk-table style="margin-top: 15px;"
                  :data="tplList"
                  :size="size"
                  :pagination="pagination"
                  @page-change="handlePageChange"
                  @page-limit-change="handlePageLimitChange">
            <!--            <bk-table-column type="selection" width="60"></bk-table-column>-->
            <bk-table-column label="模板名称" prop="tpl_name"></bk-table-column>
            <bk-table-column label="系统" prop="tpl_os" :formatter="os">
            </bk-table-column>
            <bk-table-column label="操作">
                <template slot-scope="scope">
                    <bk-button theme="primary" size="small" @click="fetch_quota_list(scope.row.id)">查看指标</bk-button>
                    <bk-button theme="success" size="small" @click="add_quota(scope.row.id, scope.row.tpl_os)">新增指标
                    </bk-button>
                </template>
            </bk-table-column>
        </bk-table>
        <bk-dialog v-model="addQuotaDialogVisible" theme="primary" title="新增指标" :show-footer="false">
            <bk-form :label-width="80">
                <bk-form-item label="指标名称">
                    <bk-input v-model="tempAddQuota.quota_name"></bk-input>
                </bk-form-item>
                <bk-form-item label="指标系统">
                    <!--                    <bk-input v-model="tempAddQuota.quota_os" :disabled="true"></bk-input>-->
                    <bk-select :disabled="true" v-model="tempAddQuota.quota_os">
                        <bk-option v-for="osData in osList" :key="osData.id" :id="osData.id"
                                   :name="osData.os_name"></bk-option>
                    </bk-select>
                </bk-form-item>
                <bk-form-item label="脚本类型">
                    <bk-select v-model="tempAddQuota.script_type">
                        <bk-option v-for="script in scriptTypes" :key="script.id" :id="script.id"
                                   :name="script.name"></bk-option>
                    </bk-select>
                </bk-form-item>
                <bk-form-item label="脚本内容">
                    <bk-input :type="'textarea'" :rows="3" v-model="tempAddQuota.script_content">
                    </bk-input>
                </bk-form-item>
                <bk-form-item label="对比方式">
                    <bk-select v-model="tempAddQuota.quota_handler">
                        <bk-option v-for="h in handlers" :key="h.val" :id="h.val" :name="h.name"></bk-option>
                    </bk-select>
                </bk-form-item>
                <bk-form-item label="对比值">
                    <bk-input v-model="tempAddQuota.quota_threshold"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-button ext-cls="mr5" theme="primary" @click="addQuotaClick">提交</bk-button>
                </bk-form-item>
            </bk-form>
        </bk-dialog>

        <bk-dialog v-model="quotaListVisible" theme="primary" title="指标列表"
                   :show-footer="false" width="1200">
            <bk-table :data="quataList">
                <bk-table-column label="指标名称" prop="quota_name" width="200"></bk-table-column>
                <bk-table-column label="指标系统" prop="quota_os" :formatter="os" width="150"></bk-table-column>
                <bk-table-column label="日志处理器" prop="quota_handler" width="150"></bk-table-column>
                <bk-table-column label="比较值" prop="quota_threshold" width="150"></bk-table-column>
                <bk-table-column label="脚本类型" width="120">
                    <template slot-scope="scope">
                        {{ scriptTypes.find(t => t.id === scope.row.script_type).name }}
                    </template>
                </bk-table-column>
                <bk-table-column label="脚本内容" prop="script_content" width="380"></bk-table-column>
            </bk-table>
        </bk-dialog>

    </div>
</template>

<script>
    export default {
        name: 'list',
        data () {
            return {
                osList: [],
                tempAddQuotaTplId: 0,
                tempAddQuota: {},
                quotaListVisible: false,
                addQuotaDialogVisible: false,
                scriptTypes: [
                    { id: 1, name: 'shell脚本' },
                    { id: 2, name: 'bat脚本' },
                    { id: 3, name: 'perl脚本' },
                    { id: 4, name: 'python脚本' },
                    { id: 5, name: 'Powershell脚本' }
                ],
                handlers: [
                    { name: '数字大于', val: 'cmp_integer_gt' },
                    { name: '数字大于等于', val: 'cmp_integer_gte' },
                    { name: '数字小于', val: 'cmp_integer_lt' },
                    { name: '数字小于等于', val: 'cmp_integer_lte' },
                    { name: '数字等于', val: 'cmp_integer_eq' },
                    { name: '数字不等于', val: 'cmp_integer_neq' },
                    { name: '字符串等于', val: 'cmp_string_eq' },
                    { name: '字符串不等于', val: 'cmp_string_neq' }
                ],
                size: 'small',
                tplList: [],
                quataList: [],
                pagination: {
                    current: 1,
                    count: 500,
                    limit: 20
                }
            }
        },
        created: function () {
            this.fetch_tpl_list()
            this.get_os_list()
        },
        methods: {
            os: function (row, column, cellValue, index) {
                const self = this
                for (const val in self.osList) {
                    const os = self.osList[val]
                    const osId = row['tpl_os'] || row['quota_os']
                    // eslint-disable-next-line eqeqeq
                    if (os.id == osId) {
                        return os.os_name
                    }
                }
            },
            get_os_list: function () {
                const self = this
                const res = this.$store.dispatch('get_init_data', 'get_os_list')
                res.then(function (data) {
                    self.osList = data.data
                })
            },
            async add_quota (tplId, os) {
                this.tempAddQuotaTplId = tplId
                this.addQuotaDialogVisible = true
                this.tempAddQuota = {
                    quota_os: os,
                    script_type: 1,
                    quota_handler: 'cmp_integer_gt',
                    quota_threshold: '0'
                }
            },
            async addQuotaClick () {
                this.tempAddQuota.tpl_id = this.tempAddQuotaTplId
                await this.$store.dispatch('add_quota', this.tempAddQuota)
                this.addQuotaDialogVisible = false
            },
            async fetch_tpl_list () {
                const res = await this.$store.dispatch('fetch_tpl_list')
                const { data } = res
                this.tplList = data
            },
            async fetch_quota_list (tplId) {
                const res = await this.$store.dispatch('fetch_quota_list', { tpl_id: tplId })

                this.quataList = res.data
                this.quotaListVisible = true
            },
            handlePageLimitChange () {
                console.log('handlePageLimitChange', arguments)
            },
            handlePageChange (page) {
                this.pagination.current = page
            }
        }
    }
</script>

<style scoped>

</style>
