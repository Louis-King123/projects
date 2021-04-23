<template>
    <div class="notifyConfigContainer">
        <div class="notifyConfigFormContent">
            <div style="margin: 40px 0px 0px 100px;">
                <div style="float:left;font-size:14px;">
                    <p>消息通知渠道 <span style="color:red;">*</span></p>
                </div>
                <div style="margin-left:120px;">
                    <bk-container :col="34">
                        <bk-checkbox-group v-model="configSelect">
                        <bk-row>
                            <bk-col
                                :span="$store.getters.getOsColSpan"
                                v-for="conf in notifyConfig"
                                :key="conf.id">
                                <bk-checkbox :value="conf.type" style="margin-left:84px;"></bk-checkbox>
                                <div class="firstStepItem"
                                    @click="SelectCongfig(conf.type)">
                                    <img
                                        :src="`${$store.getters.getImgFilePath}${conf.type}.png`"
                                        alt="">
                                </div>
                            </bk-col>
                        </bk-row>
                        </bk-checkbox-group>
                    </bk-container>
                </div>
            </div>
            <div align="center">
                <bk-button
                    ext-cls="mr5"
                    theme="primary"
                    size="large"
                    class="saveButton"
                    @click.prevent="handleSubmit"
                    >
                    保存
                </bk-button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'notifyConfig',
        data () {
            return {
                configSelect: [],
                notifyConfig: []
            }
        },
        watch: {},
        async created () {
            this.fetch_nofity_configs()
        },
        methods: {
            async fetch_nofity_configs () {
                try {
                    const res = await this.$store.dispatch('fetch_notify_config')
                    const { data } = res
                    this.configSelect = data.config_values
                    this.notifyConfig = data.descriptions
                } catch (e) {
                    console.log('fetch_notify_config', e)
                }
            },
            SelectCongfig (item) {
                if (!this.configSelect.includes(item)) {
                    this.configSelect.push(item)
                } else {
                    // 查找下标删除
                    const index = this.configSelect.findIndex(selected => {
                        if (selected === item) {
                            return true
                        }
                    })
                    this.configSelect.splice(index, 1)
                }
            },
            // 更新通知配置
            async handleSubmit () {
                if (this.configSelect.length < 1) {
                    this.$bkMessage({ delay: 3000, message: '请至少选择一种通知方式', theme: 'error' })
                    return 0
                }

                try {
                    const { configSelect } = this

                    const params = {
                        notify_configs: configSelect
                    }

                    const res = await this.$store.dispatch('notify_config_update', params)

                    const { code, message } = res

                    const theme = code === 0 ? 'success' : 'error'
                    this.$bkMessage({ delay: 3000, message, theme })
                    if (code === 0) {
                        setTimeout(e => {
                            window.location.reload()
                        }, 1500)
                    }
                } catch (e) {
                    console.log('notify_config_update', e)
                }
            }
        }
    }
</script>

<style scoped>
    @import './notifyConfig.css';
</style>
