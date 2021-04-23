<template>
    <div class="monitor-navigation">
        <bk-navigation
                :header-title="nav.id"
                :side-title="nav.title"
                @hover='handleHover'
                :default-open="true"
                :navigation-type="curNav.nav"
                :need-menu="curNav.needMenu"
                @toggle="handleToggle">
            <template slot="header">
                <div class="monitor-navigation-header">
                    <ol class="header-nav" v-if="curNav.nav === 'top-bottom'">
                        <bk-popover v-for="(item,index) in header.list" :key="item.id" theme="light navigation-message"
                                    :arrow="false" offset="0, -5" placement="bottom"
                                    :tippy-options="{ 'hideOnClick': false, flipBehavior: ['bottom'] }">
                            <li v-show="item.show" class="header-nav-item"
                                :class="{ 'item-active': index === header.active }">
                                {{item.name}}
                            </li>
                            <template slot="content">
                                <ul class="monitor-navigation-nav">
                                    <li class="nav-item" v-for="headerNavItem in curHeaderNav.navList"
                                        :key="headerNavItem.id">
                                        {{headerNavItem.name}}
                                    </li>
                                </ul>
                            </template>
                        </bk-popover>
                    </ol>
                    <div v-else class="header-title">
                        <!--<span class="header-title-icon">
                            <bk-icon
                                    style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;"
                                    type="home-shape" />
                        </span>-->
                        <!--{{nav.parent}} / {{nav.id}}-->
                        <span v-if="nav.parent === ''">首页 / {{nav.id}}</span>
                        <span v-if="nav.parent !== ''">{{nav.parent}} / {{nav.id}}</span>
                    </div>
                    <div class="header-select"></div>
                    <!-- <bk-select  class="header-select" :class="{ 'is-left': curNav.nav === 'left-right' }" v-model="header.bizId" :clearable="false" searchable>
                        <bk-option v-for="option in header.selectList"
                            :key="option.id"
                            :id="option.id"
                            :name="option.name">
                        </bk-option>
                    </bk-select> -->
                    <bk-popover v-if="false" theme="light navigation-message" :arrow="false" offset="-150, 5"
                                trigger="mouseenter" :tippy-options="{ 'hideOnClick': false }">
                        <div class="header-mind" :class="{ 'is-left': curNav.nav === 'left-right' }">
                            <svg style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;"
                                 viewBox="0 0 64 64" version="1.1" xmlns="http://www.w3.org/2000/svg">
                                <path d="M32,56c-1.3,0-2.6-0.6-3.4-1.6h-4.5c0.5,1.5,1.4,2.7,2.6,3.7c3.1,2.5,7.5,2.5,10.6,0c1.2-1,2.1-2.3,2.6-3.7h-4.5C34.6,55.4,33.3,56,32,56z"></path>
                                <path d="M53.8,49.1L50,41.5V28c0-8.4-5.8-15.7-14-17.6V8c0-2.2-1.8-4-4-4s-4,1.8-4,4v2.4c-8.2,1.9-14,9.2-14,17.6v13.5l-3.8,7.6c-0.3,0.6-0.3,1.3,0.1,1.9c0.4,0.6,1,1,1.7,1h40c0.7,0,1.3-0.4,1.7-1C54,50.4,54.1,49.7,53.8,49.1z"></path>
                            </svg>
                            <span class="header-mind-mark" :class="{ 'is-left': curNav.nav === 'left-right' }"></span>
                        </div>
                        <template slot="content">
                            <div class="monitor-navigation-message">
                                <h5 class="message-title">消息中心</h5>
                                <ul class="message-list">
                                    <li class="message-list-item" v-for="(item,index) in message.list" :key="index">
                                        <span class="item-message">{{item.message}}</span>
                                        <span class="item-date">{{item.date}}</span>
                                    </li>
                                </ul>
                                <div class="message-footer">进入消息中心</div>
                            </div>
                        </template>
                    </bk-popover>
                    <div v-if="false" class="header-help" :class="{ 'is-left': curNav.nav === 'left-right' }">
                        <svg class="bk-icon"
                             style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;"
                             viewBox="0 0 64 64" version="1.1" xmlns="http://www.w3.org/2000/svg">
                            <path d="M32,4C16.5,4,4,16.5,4,32c0,3.6,0.7,7.1,2,10.4V56c0,1.1,0.9,2,2,2h13.6C36,63.7,52.3,56.8,58,42.4S56.8,11.7,42.4,6C39.1,4.7,35.6,4,32,4z M31.3,45.1c-1.7,0-3-1.3-3-3s1.3-3,3-3c1.7,0,3,1.3,3,3S33,45.1,31.3,45.1z M36.7,31.7c-2.3,1.3-3,2.2-3,3.9v0.9H29v-1c-0.2-2.8,0.7-4.4,3.2-5.8c2.3-1.4,3-2.2,3-3.8s-1.3-2.8-3.3-2.8c-1.8-0.1-3.3,1.2-3.5,3c0,0.1,0,0.1,0,0.2h-4.8c0.1-4.4,3.1-7.4,8.5-7.4c5,0,8.3,2.8,8.3,6.9C40.5,28.4,39.2,30.3,36.7,31.7z"></path>
                        </svg>
                    </div>
                    <bk-popover theme="light navigation-message" :arrow="false" offset="-20, 10"
                                placement="bottom-start" :tippy-options="{ 'hideOnClick': false }">
                        <div class="header-user" :class="{ 'is-left': curNav.nav === 'left-right' }">
                            {{ $store.getters.getUsername }}
                            <!--<i class="bk-icon icon-down-shape"></i>-->
                        </div>
                        <!--<template slot="content">
                            <ul class="monitor-navigation-admin">
                                <li class="nav-item" v-for="userItem in user.list" :key="userItem">
                                    {{userItem}}
                                </li>
                            </ul>
                        </template>-->
                    </bk-popover>
                </div>
            </template>
            <template slot="menu">
                <bk-navigation-menu
                        ref="menu"
                        @select="handleSelect"
                        :default-active="nav.id"
                        :before-nav-change="beforeNavChange"
                        :toggle-active="nav.toggle">
                    <bk-navigation-menu-item
                            v-for="item in nav.list"
                            :key="item.name"
                            :has-child="item.children && !!item.children.length"
                            :group="item.group"
                            :icon="item.icon"
                            :disabled="item.disabled"
                            :url="baseUrl + item.url"
                            :id="item.name">
                        <span>{{item.name}}</span>
                        <div slot="child">
                            <bk-navigation-menu-item
                                    :key="child.name"
                                    v-for="child in item.children"
                                    v-show="!child.hasOwnProperty('isShow') && child.isShow !== false"
                                    :id="child.name"
                                    :url="baseUrl + child.url"
                                    :disabled="child.disabled"
                                    :icon="child.icon"
                                    :default-active="child.active">
                                <span>{{child.name}}</span>
                            </bk-navigation-menu-item>
                        </div>
                    </bk-navigation-menu-item>
                </bk-navigation-menu>
            </template>
            <div class="monitor-navigation-content" style="background-color: #F2F2F2D8;">
                <!--<div class="header-title" style="font-size: smaller;border-bottom: 1px rgba(233, 233, 233, 1) solid;background-color: white;height:62px;position: relative;">
                    <span style="font-weight: 600;font-style: normal;font-size: 14px;color: #00000072;line-height: 62px;padding:0 0 0 32px;">{{nav.parent}} / {{nav.id}}</span>
                    &lt;!&ndash;<br>
                    <span style="font-weight: 600;font-style: normal;font-size: 18px;color: #000000D8;line-height: 40px;padding:0 0 0 32px;">{{nav.parent}}</span>&ndash;&gt;

                    <div class="goBackBtn" v-show="isDetail">
                      <bk-button theme="primary" @click="handleGoBack" size="small">返回</bk-button>
                    </div>
                </div>-->
                <main class="main-content"  v-bkloading="{ isLoading: mainContentLoading, opacity: 1 }">
                    <router-view :key="$route.path"  v-show="!mainContentLoading" />
                </main>
            </div>
            <template slot="footer">
                <div class="monitor-navigation-footer">
                    Copyright © 2012-{{new Date().getFullYear()}} 统一巡检管理. All Rights Reserved. 成都忆享科技 版权所有
                </div>
            </template>
        </bk-navigation>

        <!--返回顶部按钮-->
        <el-backtop
          target=".container-content"
          :visibility-height="300"
          :bottom="20"
          :right="30">
          <i class='el-icon-top'></i>
        </el-backtop>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex'

    export default {
        name: 'monitor-navigation',
        data () {
            return {
                baseUrl: window.PROJECT_CONFIG.SITE_URL,
                navActive: 0,
                navMap: [
                    {
                        nav: 'left-right',
                        needMenu: true,
                        name: '左右结构导航'
                    },
                    {
                        nav: 'top-bottom',
                        needMenu: true,
                        name: '上下结构导航'
                    }
                ],
                nav: {
                    list: [
                        {
                            name: '首页',
                            icon: 'icon-dashboard-shape',
                            url: '',
                            open: true
                        },
                        {
                            name: '模板管理',
                            icon: 'icon-block-shape',
                            children: [
                                {
                                    name: '新增模板',
                                    url: 'module/add',
                                    hasQuery: true
                                },
                                {
                                    name: '模板列表',
                                    url: 'module/list'
                                },
                                {
                                    name: '模板列表 / 模板详情',
                                    url: 'module/list/detail',
                                    isShow: false,
                                    hasQuery: true
                                }
                            ]
                        },
                        {
                            name: '任务管理',
                            icon: 'icon-pipeline-shape',
                            children: [
                                {
                                    name: '新增任务',
                                    url: 'job/add',
                                    hasQuery: true

                                },
                                {
                                    url: 'job/list',
                                    name: '任务列表'
                                }
                            ]
                        },
                        {
                            name: '指标管理',
                            icon: 'icon-data2-shape',
                            children: [
                                {
                                    name: '指标列表',
                                    url: 'quota/quotaList'
                                },
                                {
                                    name: '巡检对象列表',
                                    url: 'quota/osList'
                                }
                            ]
                        },
                        {
                            name: '报告管理',
                            icon: 'icon-dashboard-2-shape',
                            children: [
                                {
                                    url: 'report/history',
                                    name: '历史报告'
                                },
                                {
                                    url: 'report/check',
                                    name: '巡检报告',
                                    hasQuery: true
                                },
                                {
                                    url: 'report/linux/detail',
                                    name: 'linux详情',
                                    isShow: false,
                                    hasQuery: true
                                },
                                {
                                    url: 'report/windows/detail',
                                    name: 'windows详情',
                                    isShow: false,
                                    hasQuery: true
                                }
                            ]
                        },
                        {
                            name: '系统管理',
                            icon: 'icon-cog-shape',
                            children: [
                                {
                                    name: '操作日志',
                                    url: 'system/operateLog'
                                },
                                {
                                    name: '通知配置',
                                    url: 'system/notifyConfig'
                                }
                            ]
                        }
                    ],
                    id: '首页',
                    parent: '首页',
                    toggle: true,
                    submenuActive: true,
                    title: '统一巡检管理'
                },
                header: {
                    list: [],
                    selectList: [],
                    active: 2,
                    bizId: 1
                },
                message: {
                    list: []
                },
                user: {
                    list: [
                        '退出登录'
                    ]
                },
                hasQuery: false
            }
        },
        computed: {
            curNav () {
                return this.navMap[this.navActive]
            },
            curHeaderNav () {
                return this.header.list[this.header.active] || {}
            },
            // isDetail () {
            //     return this.$route.name === 'moduleDetail'
            // },
            ...mapGetters(['mainContentLoading'])
        },
        watch: {
            '$route': {
                handler (val) {
                    const { path } = val
                    const { baseUrl } = this

                    this.nav.list.forEach(parent => {
                        if (parent.children && parent.children.length) {
                            parent.children.forEach(child => {
                                if (baseUrl + child.url === path) {
                                    this.nav.parent = parent.name
                                    this.nav.id = child.name
                                }
                            })
                        } else {
                            this.nav.parent = parent.name
                            this.nav.id = parent.name
                        }
                    })
                },
                immediate: true
            }
        },
        created () {
            const { getUser, getOsResults } = this
            Promise.all([getUser, getOsResults].map(handler => handler()))
                .then()
                .catch()
        },
        methods: {
            ...mapActions(['getUser', 'getOsResults']),

            // handleGoBack () {
            //     this.$router.back()
            // },
            handleHover (v) {
                v = false
            },
            handleSelect (id, item) {
                const { url } = item
                const { baseUrl } = this

                this.nav.list.forEach(parent => {
                    if (parent.children && parent.children.length) {
                        parent.children.forEach(child => {
                            if (baseUrl + child.url === url) {
                                this.hasQuery = child.hasQuery
                            }
                        })
                    } else {
                        this.hasQuery = parent.hasQuery
                    }
                })

                this.$router.push({
                    path: url,
                    query: this.hasQuery ? this.$route.query : {}
                })
            },
            handleToggle (v) {
                // console.log('v=', v)
                return v
            },
            beforeNavChange (newId, oldId) {
                // console.info(newId, oldId)
                return true
            },
            handleChangeNav () {
                this.navActive = (this.navActive + 1) % 3
            }
        }
    }
</script>

<style scoped>
  /deep/.container-header {
    height: 52px !important;
  }
</style>

<style lang="postcss">
    /*.goBackBtn {
      position: absolute;
      right: 26px;
      bottom: 18px;
    }*/

    /* 以下样式是为了适应例子父级的宽高而设置  */
    .bk-navigation {
        width: calc(100vw) !important;
        height: calc(100vh) !important;
        outline: 1px solid #ebebeb;
    }

    .bk-navigation .bk-navigation-wrapper {
        height: calc(100vh - 252px) !important;
    }

    /* 以上样式是为了适应例子父级的宽高而设置 */

    .monitor-navigation-header {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        height: 100%;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        font-size: 14px;
    }

    .monitor-navigation-header .header-nav {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        padding: 0;
        margin: 0;
    }

    .monitor-navigation-header .header-nav-item {
        list-style: none;
        height: 50px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        margin-right: 40px;
        color: #96A2B9;
        min-width: 56px
    }

    .monitor-navigation-header .header-nav-item.item-active {
        color: #FFFFFF !important;
    }

    .monitor-navigation-header .header-nav-item:hover {
        cursor: pointer;
        color: #D3D9E4;
    }

    .monitor-navigation-header .header-title {
        color: #63656E;
        font-size: 16px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        margin-left: -6px;
    }

    .monitor-navigation-header .header-title-icon {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        width: 28px;
        height: 28px;
        font-size: 28px;
        color: rgb(24, 33, 50);
        cursor: pointer;
    }

    .monitor-navigation-header .header-select {
        width: 240px;
        margin-left: auto;
        margin-right: 34px;
        border: none;
        background: #252F43;
        color: #D3D9E4;
        -webkit-box-shadow: none;
        box-shadow: none
    }

    .monitor-navigation-header .header-select.is-left {
        background: #F0F1F5;
        color: #63656E;
    }

    .monitor-navigation-header .header-mind {
        color: #768197;
        font-size: 16px;
        position: relative;
        height: 32px;
        width: 32px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        margin-right: 8px
    }

    .monitor-navigation-header .header-mind.is-left {
        color: #63656E;
    }

    .monitor-navigation-header .header-mind.is-left:hover {
        color: #3A84FF;
        background: #F0F1F5
    }

    .monitor-navigation-header .header-mind-mark {
        position: absolute;
        right: 8px;
        top: 8px;
        height: 7px;
        width: 7px;
        border: 1px solid #27334C;
        background-color: #EA3636;
        border-radius: 100%
    }

    .monitor-navigation-header .header-mind-mark.is-left {
        border-color: #F0F1F5;
    }

    .monitor-navigation-header .header-mind:hover {
        background: -webkit-gradient(linear, right top, left top, from(rgba(37, 48, 71, 1)), to(rgba(38, 50, 71, 1)));
        background: linear-gradient(270deg, rgba(37, 48, 71, 1) 0%, rgba(38, 50, 71, 1) 100%);
        border-radius: 100%;
        cursor: pointer;
        color: #D3D9E4;
    }

    .monitor-navigation-header .header-help {
        color: #768197;
        font-size: 16px;
        position: relative;
        height: 32px;
        width: 32px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        margin-right: 8px
    }

    .monitor-navigation-header .header-help.is-left {
        color: #63656E;
    }

    .monitor-navigation-header .header-help.is-left:hover {
        color: #3A84FF;
        background: #F0F1F5
    }

    .monitor-navigation-header .header-help:hover {
        background: -webkit-gradient(linear, right top, left top, from(rgba(37, 48, 71, 1)), to(rgba(38, 50, 71, 1)));
        background: linear-gradient(270deg, rgba(37, 48, 71, 1) 0%, rgba(38, 50, 71, 1) 100%);
        border-radius: 100%;
        cursor: pointer;
        color: #D3D9E4;
    }

    .monitor-navigation-header .header-user {
        height: 100%;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        color: #96A2B9;
        margin-left: 8px;
    }

    .monitor-navigation-header .header-user .bk-icon {
        margin-left: 5px;
        font-size: 12px;
    }

    .monitor-navigation-header .header-user.is-left {
        color: #63656E;
    }

    .monitor-navigation-header .header-user.is-left:hover {
        color: #3A84FF
    }

    .monitor-navigation-header .header-user:hover {
        cursor: pointer;
        color: #D3D9E4;
    }

    .monitor-navigation-content {
        min-height: calc(100vh - 59px - 52px - 32px - 1px) !important;
        /* padding: 15px; */
        background: #FFFFFF;
        -webkit-box-shadow: 0px 2px 4px 0px rgba(25, 25, 41, 0.05);
        box-shadow: 0px 2px 4px 0px rgba(25, 25, 41, 0.05);
        border-radius: 2px;
        border: 1px solid rgba(220, 222, 229, 1);
    }

    .monitor-navigation-footer {
        height: 52px;
        width: 100%;
        margin: 32px 0 0;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        border-top: 1px solid #DCDEE5;
        color: #63656E;
        font-size: 12px;
    }

    .monitor-navigation-message {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        width: 360px;
        background-color: #FFFFFF;
        border: 1px solid #E2E2E2;
        border-radius: 2px;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        color: #979BA5;
        font-size: 12px;
    }

    .monitor-navigation-message .message-title {
        -webkit-box-flex: 0;
        -ms-flex: 0 0 48px;
        flex: 0 0 48px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        color: #313238;
        font-size: 14px;
        padding: 0 20px;
        margin: 0;
        border-bottom: 1px solid #F0F1F5;
    }

    .monitor-navigation-message .message-list {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        max-height: 450px;
        overflow: auto;
        margin: 0;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        padding: 0;
    }

    .monitor-navigation-message .message-list-item {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        width: 100%;
        padding: 0 20px;
    }

    .monitor-navigation-message .message-list-item .item-message {
        padding: 13px 0;
        line-height: 16px;
        min-height: 42px;
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        -ms-flex-wrap: wrap;
        flex-wrap: wrap;
        color: #63656E;
    }

    .monitor-navigation-message .message-list-item .item-date {
        padding: 13px 0;
        margin-left: 16px;
        color: #979BA5;
    }

    .monitor-navigation-message .message-list-item:hover {
        cursor: pointer;
        background: #F0F1F5;
    }

    .monitor-navigation-message .message-footer {
        -webkit-box-flex: 0;
        -ms-flex: 0 0 42px;
        flex: 0 0 42px;
        border-top: 1px solid #F0F1F5;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        color: #3A84FF;
    }

    .monitor-navigation-nav {
        width: 150px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        background: #FFFFFF;
        border: 1px solid #E2E2E2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656E;
    }

    .monitor-navigation-nav .nav-item {
        -webkit-box-flex: 0;
        -ms-flex: 0 0 32px;
        flex: 0 0 32px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        padding: 0 20px;
        list-style: none
    }

    .monitor-navigation-nav .nav-item:hover {
        color: #3A84FF;
        cursor: pointer;
        background-color: #F0F1F5;
    }

    .monitor-navigation-admin {
        width: 170px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        background: #FFFFFF;
        border: 1px solid #E2E2E2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656E;
    }

    .monitor-navigation-admin .nav-item {
        -webkit-box-flex: 0;
        -ms-flex: 0 0 32px;
        flex: 0 0 32px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        padding: 0 20px;
        list-style: none
    }

    .monitor-navigation-admin .nav-item:hover {
        color: #3A84FF;
        cursor: pointer;
        background-color: #F0F1F5;
    }

    .tippy-popper .tippy-tooltip.navigation-message-theme {
        padding: 0;
        border-radius: 0;
        -webkit-box-shadow: none;
        box-shadow: none;
    }

    .bk-navigation-wrapper .navigation-container .container-content {
        padding: 0px;
        width: 100%;
        height: 100vh;
        overflow-x: hidden;
    }

    .nav-slider-footer {
        /* display: none !important; */
    }
</style>
