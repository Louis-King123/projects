/**
 * @file router 配置
 * @author konghongbo <1506637167@163.com>
 */

import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '@/store'
import http from '@/api'
import preload from '@/common/preload'

Vue.use(VueRouter)
const Home = () => import('@/views/home')
const moduleAdd = () => import('@/views/module/add')
const moduleList = () => import('@/views/module/list')
const moduleDetail = () => import('@/views/module/detail')
const jobAdd = () => import('@/views/job/add')
const jobList = () => import('@/views/job/list')
const quotaList = () => import('@/views/quota/quotaList')
const osList = () => import('@/views/quota/osList')
const checkReport = () => import('@/views/report/checkReport')
const historyReport = () => import('@/views/report/historyReport')
const reportLinuxDetail = () => import('@/views/report/reportLinuxDetail')
const reportWindowsDetail = () => import('@/views/report/reportWindowsDetail')
const operateLog = () => import('@/views/system/operateLog')
const notifyConfig = () => import('@/views/system/notifyConfig')
const MainEntry = () => import(/* webpackChunkName: 'entry' */'@/views')
const NotFound = () => import(/* webpackChunkName: 'none' */'@/views/404')

const routes = [
    {
        path: window.PROJECT_CONFIG.SITE_URL,
        name: 'appMain',
        component: MainEntry,
        alias: '',
        children: [
            {
                path: 'home',
                alias: '',
                name: 'home',
                component: Home
            },
            {
                path: 'module/add',
                alias: '',
                name: 'moduleAdd',
                component: moduleAdd
            },
            {
                path: 'module/list',
                alias: '',
                name: 'moduleList',
                component: moduleList
            },
            {
                path: 'module/list/detail',
                alias: '',
                name: 'moduleDetail',
                component: moduleDetail
            },
            {
                path: 'job/add',
                alias: '',
                name: 'jobAdd',
                component: jobAdd
            },
            {
                path: 'job/list',
                alias: '',
                name: 'jobList',
                component: jobList
            },
            {
                path: 'quota/quotaList',
                alias: '',
                name: 'quotaList',
                component: quotaList
            },
            {
                path: 'quota/osList',
                alias: '',
                name: 'osList',
                component: osList
            },
            {
                path: 'report/check',
                alias: '',
                name: 'checkReport',
                component: checkReport
            },
            {
                path: 'report/history',
                alias: '',
                name: 'historyReport',
                component: historyReport
            },
            {
                path: 'report/linux/detail',
                alias: '',
                name: 'linuxDetailReport',
                component: reportLinuxDetail
            },
            {
                path: 'report/windows/detail',
                alias: '',
                name: 'windowsDetailReport',
                component: reportWindowsDetail
            },
            {
                path: 'system/operateLog',
                alias: '',
                name: 'operateLog',
                component: operateLog
            },
            {
                path: 'system/notifyConfig',
                alias: '',
                name: 'notifyConfig',
                component: notifyConfig
            }
        ]
    },
    // 404
    {
        path: '*',
        name: '404',
        component: NotFound
    }
]

const router = new VueRouter({
    mode: 'history',
    routes: routes
})

const cancelRequest = async () => {
    const allRequest = http.queue.get()
    const requestQueue = allRequest.filter(request => request.cancelWhenRouteChange)
    await http.cancel(requestQueue.map(request => request.requestId))
}

let preloading = true
let canceling = true
let pageMethodExecuting = true

router.beforeEach(async (to, from, next) => {
    canceling = true
    await cancelRequest()
    canceling = false
    next()
})

router.afterEach(async (to, from) => {
    store.commit('setMainContentLoading', true)

    preloading = true
    await preload()
    preloading = false

    const pageDataMethods = []
    const routerList = to.matched
    routerList.forEach(r => {
        Object.values(r.instances).forEach(vm => {
            if (typeof vm.fetchPageData === 'function') {
                pageDataMethods.push(vm.fetchPageData())
            }
            if (typeof vm.$options.preload === 'function') {
                pageDataMethods.push(vm.$options.preload.call(vm))
            }
        })
    })

    pageMethodExecuting = true
    await Promise.all(pageDataMethods)
    pageMethodExecuting = false

    if (!preloading && !canceling && !pageMethodExecuting) {
        store.commit('setMainContentLoading', false)
    }
})

export default router
