<template>
    <div class="profile-page">
        <section class="section-profile-cover section-shaped my-0">
            <div class="shape shape-style-1 shape-primary shape-skew alpha-4">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        </section>
        <section class="section section-skew">
            <div class="container">
                <card shadow class="card-profile mt--300" no-body>
                    <div class="px-4">
                        <div class="text-center mt-5">
                            <h3>Geolocation App
                            </h3>
                            <div class="h6 font-weight-300"><i class="ni location_pin mr-2"></i>App to find things</div>
                            <div class="h6 mt-4"><i class="ni business_briefcase-24 mr-2"></i>Lots of thins</div>
                            <div><i class="ni education_hat mr-2"></i>And Lots of things</div>
                        </div>
                        <div class="mt-5 py-5 border-top text-center">
                            <div class="row justify-content-center">
                                <div class="col-lg-9">
                                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris feugiat ultrices
                                        scelerisque. Maecenas lacinia in urna ac porttitor. Vestibulum id congue sem, in
                                        dictum odio. Quisque vitae lorem vel velit viverra lobortis. Duis eu odio id leo
                                        sodales ultricies in nec turpis. Donec a finibus nunc. Phasellus sed volutpat
                                        orci. Vivamus semper dapibus tellus.

                                        Integer vulputate sed tortor quis ultrices. Proin nec purus in eros pulvinar
                                        lacinia et eget quam. Cras nulla sem, sodales sed arcu sit amet, lacinia
                                        efficitur enim. Donec bibendum purus sit amet nunc interdum feugiat. Duis
                                        tincidunt non nisi eget ultricies. Nam placerat euismod dapibus. Cras dolor
                                        nisl, vestibulum a ligula in, pharetra vehicula magna. Sed luctus in sapien at
                                        sagittis. Mauris tristique blandit massa in fringilla. Ut et gravida ex. Donec
                                        varius eleifend posuere. Suspendisse molestie, arcu non molestie varius, sapien
                                        tellus mattis enim, id dapibus odio dui ac tellus. Proin odio ante, dignissim a
                                        velit at, interdum dictum quam.
                                    </p>
                                    <div class="large-12 medium-12 small-12 cell">
                                        <label>File
                                            <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
                                        </label>
                                        <base-button type="primary" v-on:click="submitFile()">Submit</base-button>
                                    </div>
                                    <b-form-textarea
                                            id="textarea"
                                            v-model="text"
                                            placeholder="Enter something..."
                                            rows="3"
                                            max-rows="6"
                                    ></b-form-textarea>

                                    <pre class="mt-3 mb-0">{{ text }}</pre>
                                    <base-button type="primary" @click="sendLocationRequest(this.text)">Get Location
                                    </base-button>
                                </div>
                                <div class="d-flex justify-content-around wrapper-jexcel" id="spread">
                                    <div id="spreadsheet" ref="spreadsheet"></div>
                                </div>
                                <VueTabulator v-model="tdata" :options="options"
                                              :integration="{ updateStrategy: 'REPLACE`' }"/>
                                <base-button type="primary" @click="runBatchSearch()">Search
                                </base-button>
                                <base-button type="primary" @click="addRow()">Add Row
                                </base-button>
                            </div>
                        </div>
                    </div>
                </card>
            </div>
        </section>
        <div>

        </div>
    </div>
</template>
<script>
    import axios from 'axios';

    let tableData = [
        {id: 1, search: "", lat: "", lon: ""},
        {id: 2, search: "", lat: "", lon: ""},
        {id: 3, search: "", lat: "", lon: ""},
        {id: 4, search: "", lat: "", lon: ""},
        {id: 5, search: "", lat: "", lon: ""},

    ]

    // const token = '40abc2724e8a87'
    // const token =  "d6a28a58bb22cbf5c3a2d2917f178e62"
    // https://locationiq.org/v1/search.php?key=40abc2724e8a87&q=Statue%20of%20Liberty&format=json

    let token = process.env.VUE_APP_LIQ_TOKEN

    import {TabulatorComponent} from "vue-tabulator";

    export default {
        components: {
            'AwesomeLocalTable': TabulatorComponent
        },
        data() {
            return {
                file: '',
                text: '',
                tdata: tableData,
                options: {
                    height: "311px",
                    layout: "fitColumns",
                    columns: [
                        {title: "Search Address", field: "search", editor: true},
                        {title: "Latitude", field: "lat", editor: true},
                        {title: "Longitude", field: "lon", editor: true}
                    ],
                }
            }
        },
        methods: {
            stringBuilder(search) {
                console.log(string)
                return 'https://locationiq.org/v1/search.php?key=' + token + '&q=' + search + '&format=json'
            },
            handleFileUpload() {
                this.file = this.$refs.file.files[0];
            },
            submitFile() {
                /*
                        Initialize the form data
                    */
                let formData = new FormData();

                /*
                    Add the form data we need to submit
                */
                formData.append('file', this.file);

                /*
                  Make the request to the POST /single-file URL
                */
                axios.post('/api/files/',
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(response => {
                    console.log('SUCCESS!!');
                    console.log(response);
                })
                    .catch(function () {
                        console.log('FAILURE!!');
                    });
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
            batchSearch(searches) {
                for (let i = 0; i < searches.length; i++) {
                    axios.get(this.stringBuilder(searches[i])).then(result => {
                            console.log(result.data);
                            let latlon = this.getLongLat(result.data);
                            console.log(latlon);
                            // this.tdata[i] = {id: i, search: searches[i], lat: latlon[0], lon: latlon[1]};
                            this.$set(this.tdata, i, {id: i, search: searches[i], lat: latlon[0], lon: latlon[1]});
                        }
                    )

                }
            },
            getLongLat(searchResult) {
                let topRes = searchResult[0];
                return [topRes.lat, topRes.lon];
            },
            addRow() {
                this.$set(this.tdata, this.tdata.length, {id: this.tdata.length, search: "", lat: "", lon: ""});

            }
        },
        created() {
            vm.component = this
        },
    }
</script>
<style>
</style>
