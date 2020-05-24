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
    dt_post(data,callback) {
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

    }


}