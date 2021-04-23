<template>
  <!-- 容器 -->
  <div class="moduleDetailContainer" v-bkloading="{ isLoading: isLoading, zIndex: 10 }">
    <!-- 标题，按钮 -->
    <div class="moduleDetailItem mb20 btnContainer">
      <h5 class="m0">模板详情</h5>
      <bk-button theme="primary" @click="handleGoBack" size="small">返回</bk-button>
    </div>
    <!--/ 标题，按钮 -->

    <!-- content -->
    <bk-collapse v-model="activeName">
      <div class="moduleDetailItem mb20" v-for="v in tplData" :key="v.id">
        <bk-collapse-item :name="v['class_name']">
          <h4 class="m0">{{ v['class_name'] }}</h4>
          <div slot="content" class="f13 pb10">
            <bk-table :data="v.children">
              <bk-table-column label="检查项" prop="quota_name"></bk-table-column>
              <bk-table-column label="对比方式">
                <template slot-scope="scope">
                  <span>{{ setQuotaHandler(scope.row['quota_handler']) }}</span>
                </template>
              </bk-table-column>
              <bk-table-column label="推荐值" prop="quota_threshold"></bk-table-column>
            </bk-table>
          </div>
        </bk-collapse-item>
      </div>
    </bk-collapse>
    <!-- /content -->
  </div>
  <!-- /容器 -->
</template>

<script>
    export default {
        name: 'detail',
        data () {
            return {
                activeName: [],
                tplId: null,
                tplInfo: {},
                tplData: [],
                isLoading: false
            }
        },
        created () {
            const { id } = this.$route.query
            if (id) {
                this.tplId = id

                const params = {
                    tpl_id: id
                }
                this.tpl_info(params)
            }
        },
        methods: {
            handleGoBack () {
                this.$router.back()
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

            // 获取模板详情
            async tpl_info (params) {
                try {
                    this.isLoading = true
                    const res = await this.$store.dispatch('tpl_info', params)
                    const { data } = res
                    this.tplInfo = data

                    if (this.tplInfo['tpl_quotas']) {
                        this.tplInfo['tpl_quotas'].forEach(v => {
                            this.tplData.push(v)
                            this.activeName.push(v['class_name'])
                        })
                    }
                } catch (e) {
                    console.log('tpl_info=', e)
                } finally {
                    this.isLoading = false
                }
            }
        }
    }
</script>

<style scoped>
  @import './detail.css';
</style>
