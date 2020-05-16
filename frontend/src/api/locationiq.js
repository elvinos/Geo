import axios from 'axios';

let token = process.env.VUE_APP_LIQ_TOKEN


export default {
    stringBuilder(search) {
        return 'https://locationiq.org/v1/search.php?key=' + token + '&q=' + search + '&format=json'
    },
    async sendLocationRequest(search) {
        let string = 'https://locationiq.org/v1/search.php?key=' + token + '&q=' + search + '&format=json'
        console.log(string)
        await axios
            .get(string)

            .then(response => {
                // this.text = response.lat
                console.log(response)
                return response.data
            })
            .catch(error => {
                console.log(error)
                // this.errored = true
            })
    },
    getSearch() {
        let searches = []
        for (let i = 0; i < this.tdata.length; i++) {
            let item = this.tdata[i];
            if (item.search !== '') {
                searches.push(item.search);
            }
        }
        console.log(searches)
        return searches
    },
    runBatchSearch() {
        this.batchSearch(this.getSearch())
    },
    async batchSearch(searches) {
        let newData = [];
        for (let i = 0; i < searches.length; i++) {
            axios.get(this.stringBuilder(searches[i])).then(result => {
                    console.log(result.data);
                    let latlon = this.getLongLat(result.data);
                    console.log(latlon);
                    newData.push({id: i, search: searches[i], lat: latlon[0], lon: latlon[1]})
                    // this.tdata[i] = {id: i, search: searches[i], lat: latlon[0], lon: latlon[1]};
                    // this.$set(this.tdata, i, {id: i, search: searches[i], lat: latlon[0], lon: latlon[1]});
                }
            )
            await this.sleep(1000)

        }
        return newData
    },
    async queryCoordinatesLocationIQ(search,i, callback){
          axios.get(this.stringBuilder(search)).then(result => {
                let latlon = this.getLongLat(result.data);
                console.log(latlon);
                callback(i, search, latlon)
                }
            )
    },

    returnData(data){
        return(data)
    },
    getLongLat(searchResult) {
        let topRes = searchResult[0];
        return [topRes.lat, topRes.lon];
    },

     sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
},

}