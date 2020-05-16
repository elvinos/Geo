import axios from 'axios'

const state = () => ({
    rowData: []
})

const getters = {}

const actions = {
    loadFiles({commit}) {
        axios
            .get('api/files/')
            .then(data => {
                let rowData = data.data
                commit('SET_FILES', rowData)
                console.log(data.data)
            })
            .catch(error => {
                console.log(error)
            })
    },
    postFile({dispatch, commit}, newFile) {
        const config = {
            onUploadProgress(e) {
                var percentCompleted = Math.round((e.loaded * 5000) / e.total);
            }
        };
        try {
            axios.post('api/files/', newFile, config,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(res => {
                    commit('POST_FILE', newFile)
                })
                .then(res => {
                    dispatch('loadFiles')
                })
        } catch (error) {
            console.log(error);
        }
    }
    ,

    deleteFile({dispatch}, result_id) {
        axios.delete('api/files/' + result_id)
            .then(res => {
                dispatch('loadFiles')
                console.log(res)
            })
            .catch(error => {
                console.log(error)
            })
    }
    ,

    downloadFile({dispatch}, filename) {
        axios({
            url: `media/${filename}`,
            method: 'GET',
            responseType: 'blob',
        })
            .then((res) => {
                const url = window.URL.createObjectURL(new Blob([res.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', filename)
                document.body.appendChild(link)
                link.click()
            })
    }
}
const mutations = {
    SET_FILES(state, files) {
        state.rowData = files
    }
    ,
    POST_FILE(state, newFile) {
        state.rowData.push(newFile)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}