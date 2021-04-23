/**
 * @file main store
 * @author konghongbo <1506637167@163.com>
 */

import Vue from 'vue'
import Vuex from 'vuex'

import example from './modules/example'
import settings from './modules/settings'
import userInfo from './modules/user'
import commonData from './modules/commonData'

import http from '@/api'
import { unifyObjectStyle } from '@/common/util'

Vue.use(Vuex)

const store = new Vuex.Store({
    // 模块
    modules: {
        example,
        settings,
        userInfo,
        commonData
    },
    // 公共 store
    state: {
        mainContentLoading: false,
        // 系统当前登录用户
        user: {}
    },
    // 公共 getters
    getters: {
        mainContentLoading: state => state.mainContentLoading,
        user: state => state.user
    },
    // 公共 mutations
    mutations: {
        /**
         * 设置内容区的 loading 是否显示
         *
         * @param {Object} state store state
         * @param {boolean} loading 是否显示 loading
         */
        setMainContentLoading (state, loading) {
            state.mainContentLoading = loading
        },

        /**
         * 更新当前用户 user
         *
         * @param {Object} state store state
         * @param {Object} user user 对象
         */
        updateUser (state, user) {
            state.user = Object.assign({}, user)
        }
    },
    actions: {
        /**
         * 获取初始数据
         */
        get_init_data (context, urlFunction, params = {}) {
            const url = '/api/' + urlFunction
            return http.get(url)
        },
        /**
         * 获取用户信息
         *
         * @param {Object} context store 上下文对象 { commit, state, dispatch }
         *
         * @return {Promise} promise 对象
         */
        userInfo (context, config = {}) {
            // ajax 地址为 USER_INFO_URL，如果需要 mock，那么只需要在 url 后加上 AJAX_MOCK_PARAM 的参数，
            // 参数值为 mock/ajax 下的路径和文件名，然后加上 invoke 参数，参数值为 AJAX_MOCK_PARAM 参数指向的文件里的方法名
            // 例如本例子里，ajax 地址为 USER_INFO_URL，mock 地址为 USER_INFO_URL?AJAX_MOCK_PARAM=index&invoke=getUserInfo

            // 后端提供的地址
            // const url = USER_INFO_URL
            // mock 的地址，示例先使用 mock 地址
            // const mockUrl = USER_INFO_URL + (USER_INFO_URL.indexOf('?') === -1 ? '?' : '&') + AJAX_MOCK_PARAM + '=index&invoke=getUserInfo'
            // return http.get(mockUrl, {}, config).then(response => {
            //     const userData = response.data || {}
            //     context.commit('updateUser', userData)
            //     return userData
            // })
        },

        // fetch_inspection_detail_windows (context, params, config = {}) {
        //     const url = '/api/fetch_inspection_detail'
        //     return http.post(url, params, config)
        // },
        fetch_inspection_os (context, params, config = {}) {
            let url = `/api/inspection_os?current=${params['current']}&limit=${params['limit']}`
            if (params['os_name']) url = `${url}&os_name=${params['os_name']}`
            return http.get(url)
        },
        update_inspection_os (context, params, config = {}) {
            const url = '/api/inspection_os'
            return http.post(url, params, config)
        },

        fetch_bk_users (context, params, config = {}) {
            const url = '/bk_users'
            return http.get(url)
        },

        fetch_business_list (context, params, config = {}) {
            const url = '/api/business_list'
            return http.get(url)
        },

        fetch_operation_log (context, params, config = {}) {
            let url = `/api/operation_log?current=${params['current']}&limit=${params['limit']}`
            if (params['start_time']) url = `${url}&start_time=${params['start_time']}&end_time=${params['end_time']}`
            if (params['operator']) url = `${url}&operator[]=${params['operator']}`
            if (params['operation_module']) url = `${url}&operation_module=${params['operation_module']}`
            if (params['request_method']) url = `${url}&request_method=${params['request_method']}`
            return http.get(url)
        },

        get_username (context, config) {
            const url = '/login_username'
            return http.get(url)
        },

        get_task (context, params, config = {}) {
            const url = '/api/task_detail?task_id=' + params['id']
            return http.get(url)
        },
        get_os_list (context, config = {}) {
            const url = '/api/get_os_list'
            return http.get(url)
        },

        // fetch_os_quota (context, params, config = {}) {
        //     const url = `/api/featch_os_quota?os_id=${params['id']}`
        //     return http.get(url)
        // },
        fetch_os_quota (context, params, config = {}) {
            const url = `/api/quota?os_id=${params['id']}`
            return http.get(url)
        },

        fetch_custom_quota (context, params, config = {}) {
            let url = `/api/quota?current=${params['current']}&limit=${params['limit']}`
            if (params['os_id']) url = `${url}&os_id=${params['os_id']}`
            if (params['tpl_id']) url = `${url}&tpl_id=${params['tpl_id']}`
            if (params['customize']) url = `${url}&customize=${params['customize']}`
            return http.get(url)
        },

        custom_quota_add (context, params, config = {}) {
            const url = '/api/quota'
            return http.post(url, params, config)
        },

        custom_quota_update (context, params, config = {}) {
            const url = '/api/quota'
            return http.put(url, params, config)
        },

        custom_quota_delete (context, params, config = {}) {
            const url = `/api/quota?quota_id=${params['quota_id']}`
            return http.delete(url)
        },

        getCountObj (context, config = {}) {
            // 后端提供的地址
            const url = 'get_count_obj'
            return http.get(url)
        },
        fetch_tpl_list (context, params = {}) {
            let url = '/api/fetch_tpl_list'
            if (params['os_id']) {
                url = `${url}?os_id=${params['os_id']}`
            }
            return http.get(url)
        },
        fetch_quota_by_tpl (context, params, config = {}) {
            const url = '/api/fetch_quota_by_tpl?tpl_id=' + params['tpl_id']
            return http.get(url)
        },
        fetch_quota_list (context, params, config = {}) {
            const url = '/api/fetch_quota_list?tpl_id=' + params['tpl_id']
            return http.get(url)
        },
        add_quota (context, params, config = {}) {
            const url = '/api/add_quota'
            return http.post(url, params, config)
        },
        tpl_info (context, params, config = {}) {
            const url = `/api/tpl?tpl_id=${params['tpl_id']}`
            return http.get(url)
        },
        tpl_add (context, params, config = {}) {
            const url = '/api/tpl'
            return http.post(url, params, config)
        },
        tpl_update (context, params, config = {}) {
            const url = '/api/tpl'
            return http.put(url, params, config)
        },
        tpl_delete (context, params, config = {}) {
            const url = `/api/tpl?tpl_id=${params['tpl_id']}`
            return http.delete(url)
        },
        execute_del (context, params, config = {}) {
            const url = `/api/task_delete?task_id=${params['task_id']}`
            return http.get(url)
        },
        execute_stop (context, params, config = {}) {
            const url = `/api/off_button?task_id=${params['task_id']}`
            return http.get(url)
        },
        search_host_by_biz (context, params, config = {}) {
            const url = '/api/search_host_by_biz'
            return http.get(url)
        },
        task_add (context, params, config = {}) {
            const url = '/api/task_add'
            return http.post(url, params, config)
        },
        // fetch_task_list (context, params, config = {}) {
        //     const url = '/api/fetch_task_list?biz_id=' + params['formData']['biz_id']
        //         + '&date=' + params['formData']['date']
        //         + '&exec_state=' + params['formData']['exec_state']
        //         + '&keywords=' + params['formData']['keywords']
        //         + '&os_id=' + params['formData']['os_id']
        //         + '&tpl_id=' + params['formData']['tpl_id']
        //         + '&page=' + params['pagination']['current']
        //         + '&size=' + params['pagination']['limit']
        //
        //     return http.get(url)
        // },
        fetch_task_list (context, params, config = {}) {
            let url = `/api/fetch_task_list?page=${params.page}&size=${params.size}`
            if (params['biz_id']) url = `${url}&biz_id=${params['biz_id']}`
            if (params['os_id']) url = `${url}&os_id=${params['os_id']}`
            if (params['exec_state']) url = `${url}&exec_state=${params['exec_state']}`
            if (params['tpl_id']) url = `${url}&tpl_id=${params['tpl_id']}`
            if (params['date']) url = `${url}&date=${params['date']}`
            if (params['keywords']) url = `${url}&keywords=${params['keywords']}`

            return http.get(url)
        },
        fetch_report (context, params, config = {}) {
            const url = '/api/fetch_report'
            return http.post(url, params, config)
        },
        execute_task (context, params, config = {}) {
            const url = '/api/execute_task'
            return http.post(url, params, config)
        },
        fetch_inspection_report_by_id (context, params, config = {}) {
            // 根据历史报告ID获取巡检报告的信息
            const url = '/api/fetch_inspection_report?id=' + params['report_id']
            return http.get(url)
        },
        search_history_list (context, params, config = {}) {
            // 根据条件搜索历史报告的列表
            const url = '/api/fetch_history_report'
            return http.post(url, params, config)
        },
        fetch_history_list (context, params, config = {}) {
            // 获取历史报告列表
            let url = `/api/fetch_history_report?current=${params['current']}&limit=${params['limit']}`
            if (params['task_tpl']) url = `${url}&task_tpl=${params['task_tpl']}`
            if (params['task_os']) url = `${url}&task_os=${params['task_os']}`
            if (params['exec_biz_id']) url = `${url}&exec_biz_id=${params['exec_biz_id']}`
            if (params['start_time']) url = `${url}&start_time=${params['start_time']}`
            if (params['end_time']) url = `${url}&end_time=${params['end_time']}`
            return http.get(url)
        },
        fetch_inspection_report_detail (context, params, config = {}) {
            // 根据条件搜索历史报告的列表
            const url = '/api/fetch_inspection_detail'
            return http.post(url, params, config)
        },
        fetch_check_activity (context, params, config = {}) {
            // 根据条件搜索历史报告的列表
            const url = '/api/fetch_check_activity'
            return http.post(url, params, config)
        },
        fetch_check_statistics (context, params, config = {}) {
            // 根据条件搜索历史报告的列表
            const url = '/api/fetch_check_statistics?start_time=' + params['start_time'] + '&end_time=' + params['end_time']
            return http.post(url, params, config)
        },
        fetch_user_list (context, params, config = {}) {
            // 根据条件搜索历史报告的列表
            const url = '/api/fetch_user_list'
            return http.post(url, params, config)
        },
        fetch_notify_config (context, params, config = {}) {
            // 查询通知配置
            const url = '/api/notify_config'
            return http.get(url)
        },
        notify_config_update (context, params, config = {}) {
            const url = '/api/notify_config'
            return http.put(url, params, config)
        }
    }
})

/**
 * hack vuex dispatch, add third parameter `config` to the dispatch method
 *
 * @param {Object|string} _type vuex type
 * @param {Object} _payload vuex payload
 * @param {Object} config config 参数，主要指 http 的参数，详见 src//api/index initConfig
 *
 * @return {Promise} 执行请求的 promise
 */
store.dispatch = function (_type, _payload, config = {}) {
    const { type, payload } = unifyObjectStyle(_type, _payload)

    const action = { type, payload, config }
    const entry = store._actions[type]
    if (!entry) {
        if (NODE_ENV !== 'production') {
            console.error(`[vuex] unknown action type: ${type}`)
        }
        return
    }

    store._actionSubscribers.forEach(sub => {
        return sub(action, store.state)
    })

    return entry.length > 1
        ? Promise.all(entry.map(handler => handler(payload, config)))
        : entry[0](payload, config)
}

export default store
