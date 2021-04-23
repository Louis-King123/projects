import http from '@/api'

const state = {
    // 巡检对象数据
    osList: []
}

const mutations = {
    setOsList (state, data) {
        state.osList = data
    }
}

const actions = {
    getOsResults ({ commit }) {
        return new Promise(resolve => {
            const url = '/api/get_os_list'
            http.get(url)
                .then(({ data }) => {
                    commit('setOsList', data)
                    resolve()
                })
                .catch(() => {})
        })
    }
}

const getters = {
    getOsList (state) {
        return state.osList
    }
}

export default {
    state,
    mutations,
    actions,
    getters
}
