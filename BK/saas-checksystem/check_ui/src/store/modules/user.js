import http from '@/api'

const state = {
    username: 'admin'
}

const mutations = {
    setUsername (state, username) {
        state.username = username
    }
}

const actions = {
    getUser ({ commit }) {
        return new Promise(resolve => {
            const url = '/login_username'
            http.get(url)
                .then(({ data }) => {
                    const { user } = data
                    commit('setUsername', user)
                    resolve()
                })
                .catch(() => {})
        })
    }
}

const getters = {
    getUsername (state) {
        return state.username
    }
}

export default {
    state,
    mutations,
    actions,
    getters
}
