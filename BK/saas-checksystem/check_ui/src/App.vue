<template>
    <div id="app" :class="systemCls">
        <router-view :key="routerKey" v-if="isRouterAlive" />
        <app-auth ref="bkAuth"></app-auth>
    </div>
</template>
<script>
    import { bus } from '@/common/bus'
    import { mapMutations } from 'vuex'

    export default {
        name: 'app',

        provide () {
            return {
                reload: this.reload
            }
        },

        data () {
            return {
                routerKey: +new Date(),
                systemCls: 'mac',
                isRouterAlive: true
            }
        },

        created () {
            this.handleResize()
            this.handleResizeConfig()

            const platform = window.navigator.platform.toLowerCase()
            if (platform.indexOf('win') === 0) {
                this.systemCls = 'win'
            }
        },

        mounted () {
            const self = this
            bus.$on('show-login-modal', data => {
                self.$refs.bkAuth.showLoginModal(data)
            })
            bus.$on('close-login-modal', () => {
                self.$refs.bkAuth.hideLoginModal()
                setTimeout(() => {
                    window.location.reload()
                }, 0)
            })
        },

        beforeDestroy () {
            this.handleResizeConfig('remove')
        },

        methods: {
            ...mapMutations(['updateOsColSpan', 'updateTplColSpan']),

            handleResizeConfig (type = 'add') {
                if (type === 'remove') return window.removeEventListener('resize', this.handleResize)

                window.addEventListener('resize', this.handleResize)
            },

            // 动态获取当前屏幕宽度
            handleResize (event) {
                this.updateOsColSpan(3)
                this.updateTplColSpan(2.4)
                const fullWidth = document.documentElement.clientWidth

                if (fullWidth < 1500) this.updateOsColSpan(4)
                if (fullWidth <= 1240) this.updateOsColSpan(6)
                if (fullWidth <= 950) this.updateOsColSpan(12)

                if (fullWidth < 1650) this.updateTplColSpan(3)
                if (fullWidth < 1430) this.updateTplColSpan(4)
                if (fullWidth <= 1200) this.updateTplColSpan(6)
                if (fullWidth <= 910) this.updateTplColSpan(12)
            },

            // 刷新页面函数
            reload () {
                this.isRouterAlive = false
                this.$nextTick(function () {
                    this.isRouterAlive = true
                })
            }
        }
    }
</script>

<style lang="postcss">
</style>
