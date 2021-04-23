<template>
    <div style="width: 600px; margin: 0 auto; margin-top: 30px;">
        <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm">
            <bk-form-item label="模板名称" :required="true" :property="'name'">
                <bk-input v-model="formData.tpl_name" placeholder="请输入3到10个以内的字符，不能为admin"></bk-input>
            </bk-form-item>
            <bk-form-item label="系统" :required="true" :property="'type'">
                <bk-select v-model="tplOs">
                    <bk-option v-for="option in typeList"
                               :key="option.id"
                               :id="option.id"
                               :name="option.os_name">
                    </bk-option>
                </bk-select>
            </bk-form-item>
            <bk-form-item>
                <bk-button ext-cls="mr5" theme="primary" title="提交" @click.stop.prevent="validate"
                           :loading="isChecking">提交
                </bk-button>
                <bk-button ext-cls="mr5" theme="default" title="清除错误提示" @click.stop.prevent="clearError">清除错误提示
                </bk-button>
            </bk-form-item>
        </bk-form>
    </div>
</template>

<script>
    export default {
        name: 'add',
        data () {
            return {
                isChecking: false,
                tplOs: 1,
                formData: {
                    tpl_name: '',
                    tpl_os: ''
                },
                typeList: [
                ],
                rules: {
                    name: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            min: 3,
                            message: function (val) {
                                return `${val}不能小于3个字符`
                            },
                            trigger: 'blur'
                        },
                        {
                            max: 10,
                            message: '不能多于10个字符',
                            trigger: 'blur'
                        },
                        {
                            validator: this.checkName,
                            message: '不能等于admin',
                            trigger: 'blur'
                        }
                    ],
                    type: [
                        {
                            required: true,
                            message: '请选择系统类型',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        watch: {
            tplOs (val) {
                this.formData.tpl_os = val
            }
        },
        created () {
            this.get_os_list()
        },
        methods: {
            get_os_list: function () {
                const self = this
                const res = this.$store.dispatch('get_init_data', 'get_os_list')
                res.then(function (data) {
                    self.typeList = data.data
                })
            },
            async checkName (val) {
                const resutl = await this.asyncCheck(val)
                return resutl
            },
            async asyncCheck (val) {
                // 模拟异步请求
                const p = new Promise((resolve, reject) => {
                    if (val === 'admin') {
                        Promise.reject(new Error(false))
                    } else {
                        resolve(true)
                    }
                })
                const result = await p.then(res => {
                    return true
                }).catch(res => {
                    return false
                })
                return result
            },
            validate () {
                this.isChecking = true
                this.$refs.validateForm.validate().then(validator => {
                    const res = this.$store.dispatch('tpl_add', this.formData)
                    console.log(res)
                    this.isChecking = false
                }, validator => {
                    this.isChecking = false
                    alert(`${validator.field}：${validator.content}`)
                })
            },
            clearError () {
                this.$refs.validateForm.clearError()
            }

        }
    }
</script>

<style scoped>

</style>
