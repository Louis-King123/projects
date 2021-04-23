const state = {
    // 静态图片地址
    imgFilePath: `${window.PROJECT_CONFIG.BK_STATIC_URL}static/images/`,

    osColSpan: 3,
    tplColSpan: 2.4
}

const mutations = {
    updateOsColSpan (state, value) {
        state.osColSpan = value
    },

    updateTplColSpan (state, value) {
        state.tplColSpan = value
    }
}

const actions = {}

const getters = {
    getImgFilePath (state) {
        return state.imgFilePath
    },

    getOsColSpan (state) {
        return state.osColSpan
    },

    getTplColSpan (state) {
        return state.tplColSpan
    }
}

export default {
    state,
    mutations,
    actions,
    getters
}
