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
                <card shadow class="card-profile" id="geolocation-card" no-body>
                    <div class="px-4">
                        <div class="text-center mt-5">
                            <h3>Geolocation App
                            </h3>
                            <div class="h6 font-weight-300"><i class="ni location_pin mr-2"></i>Convert addresses into
                                coordinates with ease for use with google maps or other applications
                            </div>

                        </div>
                        <div class="mt-5 py-5 border-top text-center">
                            <div class="mt-3 row justify-content-center">
                                <div class="h6 col-lg-9">Simply upload a csv file
                                    with your list of addresses in the first column or manually write the addresses you
                                    wish
                                    to query in the table below
                                </div>
                            </div>
                            <div class="mt-3 row justify-content-center">
                                <div class="col-lg-9">
                                    <b-form-file
                                            v-model="ufile"
                                            :state="Boolean(ufile)"
                                            placeholder="Choose a file or drop it here..."
                                            drop-placeholder="Drop file here..."
                                    ></b-form-file>
                                </div>
                            </div>
                            <div class="mt-5 row justify-content-center">
                                <div class="col-lg-9">
                                    <b-button variant="primary" @click="submitFile()">
                                        Import Address List &nbsp; &nbsp;<font-awesome-icon icon="upload"/>
                                    </b-button>
                                </div>
                            </div>
                            <div class="mt-5 row justify-content-center">
                                <VueTabulator v-model="tdata" :options="options"
                                              :integration="{ updateStrategy: 'REPLACE`' }"/>
                            </div>
                            <div class="mt-5 row justify-content-center">
                                <div class="col-lg-9">
                                    <base-button type="primary" @click="addRow()">Add Row
                                    </base-button>
                                    <base-button type="primary" @click="updateTableWCoords()">Get Coordinates
                                    </base-button>
                                    <base-button v-show="dReady" type="primary" @click="download()">Download Results
                                    </base-button>
                                </div>
                            </div>
                        </div>
                        <div v-show="dReady" class="mt-3 mb-3 row justify-content-center">
                            <div class="Map" id="gmap"/>
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
    import Papa from 'papaparse';
    import locationiq from "../api/locationiq";
    import gmapsInit from '../plugins/gmaps';

    let tableData = [
        {id: 1, search: "", lat: "", lon: ""},
        {id: 2, search: "", lat: "", lon: ""},
        {id: 3, search: "", lat: "", lon: ""},
        {id: 4, search: "", lat: "", lon: ""},
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
                ufile: null,
                file: '',
                text: '',
                dReady: false,
                tdata: tableData,
                options: {
                    // height: "400px",
                    layout: "fitColumns",
                    columns: [
                        {title: "Search Address", field: "search", editor: true, widthGrow: 2},
                        {title: "Latitude", field: "lat", editor: false, widthGrow: 1},
                        {title: "Longitude", field: "lon", editor: false, widthGrow: 1}
                    ],
                }
            }
        },
        methods: {
            async createMap() {
                try {
                    const google = await gmapsInit();
                    const geocoder = new google.maps.Geocoder();
                    const map = new google.maps.Map(document.getElementById('gmap'));
                    const bounds = new google.maps.LatLngBounds();
                    for (let i = 0; i < this.tdata.length; i++) {
                        let loc = new google.maps.LatLng(this.tdata[i]['lat'], this.tdata[i]['lon'])
                        let marker = new google.maps.Marker({
                            position: loc,
                            map: map
                        });
                        bounds.extend(loc);
                    }
                    map.fitBounds(bounds);
                    map.panToBounds(bounds);
                } catch (error) {
                    console.error(error);
                }

            },
            submitFile() {
                if (this.ufile.size < 10 * 1024 * 1024) {
                    var vm = this
                    const fd = new FormData()
                    // console.log(this.ufile)
                    fd.append('file', vm.ufile)
                    console.log(fd)
                    console.log(vm.ufile)
                    this.parseFile(vm.ufile, this.convertToTable)
                    this.$store.dispatch('fileManager/postFile', fd)
                } else {
                    alert("File size must be smaller than 10MB")
                }
            },
            printData(data) {
                // this.convertToTable(data)
                console.log(data)
            },
            convertToTable(data) {
                let newTableData = [];
                for (let i = 0; i < data.length; i++) {
                    if (data[i][0] !== "") {
                        newTableData.push({id: this.tdata.length, search: data[i][0], lat: "", lon: ""});
                    }
                }
                this.tdata = newTableData;

            },

            async parseFile(file, callBack) {
                Papa.parse(file, {
                    config: {
                        keepEmptyRows: false,
                        skipEmptyLines: true
                    },
                    complete: function (results) {
                        callBack(results.data);
                    }
                })
            },


            download() {
                var csv = Papa.unparse(this.tdata)
                let filename = "geo_results.csv";
                let blob = new Blob([csv], {
                    type: "text/plain;charset=utf-8"
                });
                const fd = new FormData()
                const file = new File([blob], filename);
                fd.append('file', file)
                this.$store.dispatch('fileManager/postFile', fd)
                let saveData = (function () {
                    let a = document.createElement("a");
                    document.body.appendChild(a);
                    a.style = "display: none";
                    return function (data, fileName) {
                        const url = window.URL.createObjectURL(data);
                        a.href = url;
                        a.download = fileName;
                        a.click();
                        window.URL.revokeObjectURL(url);
                    };
                }());
                saveData(blob, filename);
            },

            async unParseFile(file, callBack) {
                Papa.unparse(file, {
                    complete: function (results) {
                        callBack(results.data);
                    }
                })
            },

            async getLocations() {
                this.tdata = await locationiq.batchSearch(this.getSearch())
            },

            async updateTableWCoords() {
                for (let i = 0; i < this.tdata.length; i++) {
                    let item = this.tdata[i];
                    if (item.search !== '') {
                        await locationiq.queryCoordinatesLocationIQ(item.search, i, this.setData)
                    }
                    await this.sleep(1000)
                }
                this.dReady = true
                await this.createMap()
            },
            setData(i, search, latlon) {
                this.$set(this.tdata, i, {id: i, search: search, lat: latlon[0], lon: latlon[1]});
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
            addRow() {
                this.$set(this.tdata, this.tdata.length, {id: this.tdata.length, search: "", lat: "", lon: ""});
            },
            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            },
        },
        created() {
            vm.component = this
        },
    }
</script>
<style>

    .Map {
        width: 100%;
        height: 50vh;
        /*width: 30vw;*/
        /*height: 30vh;*/
    }
</style>
