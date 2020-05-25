import axios from 'axios';


export default {
    get_all_data(callback) {
        axios
            .get('api/drivetime/get_all_data')
            .then(response => {
                // console.log(response.data)
                callback(response.data)
            })
            .catch(error => {
                console.log(error)
            })

    },
    dt_post(data, callback) {
        try {
            axios.post('api/drivetime/dt_post', data,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    console.log(response.data);
                    callback(response.data)
                })
        } catch (error) {
            console.log(error);
        }

    },

    start_test(callback) {
        try {
            axios.get('api/drivetime/start_test')
                .then(response => {
                    console.log(response.data);
                    callback(response.data)
                })
        } catch (error) {
            console.log(error);
        }

    },

    update_status(task_id, callback) {
        try {
            const params = new URLSearchParams();
            params.append('task_id', task_id);
            axios.get('api/drivetime/update_status', {
                params: params
            })
                .then(response => {
                    console.log(response.data);
                    callback(response.data)
                })
        } catch (error) {
            console.log(error);
        }

    },


}