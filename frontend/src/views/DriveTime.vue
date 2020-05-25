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
                            <h3>Drive Time Analysis
                            </h3>
                            <div class="h6 font-weight-300"><i class="ni location_pin mr-2"></i>Calculate drive times
                                between locations, enabling ease of calculating average distances to competitors.
                            </div>

                        </div>
                        <div class="mt-5 py-5 border-top text-center">
                            <tabs tabNavClasses="nav-fill flex-column flex-sm-row nav-wrapper"
                                  tabContentClasses="card shadow">
                                <tab-pane id="profile">
                                    <span slot="title">
                                        <i class="ni ni-cloud-upload-96 mr-2"></i>
                                        Upload Data
                                    </span>
                                    <div class="mt-3 py-5 text-center">
                                        <div class="mt-3 row justify-content-center">
                                            <div class="h6 col-lg-9">Simply upload a csv file
                                                with your list of addresses in the first column or manually write the
                                                addresses you
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
                                    </div>
                                </tab-pane>
                                <tab-pane id="home">
                                <span slot="title">
                                    <i class="ni ni-bell-55 "></i>
                                    Paste Data From Excel/CSV File
                                </span>
                                    <div class="mt-3 py-5 row justify-content-center">
                                        <VueTabulator ref="tabulator" v-model="tdata" :options="options"
                                                      :integration="{ updateStrategy: 'REPLACE`' }"/>
                                    </div>
                                </tab-pane>
                            </tabs>
                            <div class="mt-5 row justify-content-center">
                                <div class="col-lg-9">
                                    <b-button variant="primary" @click="submitFile()">
                                        Import Address List &nbsp;&nbsp;<font-awesome-icon icon="upload"/>
                                    </b-button>
                                </div>
                            </div>
                            <div class="mt-5 row justify-content-center">
                                <div class="col-lg-9">
                                    <b-button variant="primary" @click="get_drivetime_data()">
                                        Get all data &nbsp;&nbsp;<font-awesome-icon icon="upload"/>
                                    </b-button>
                                </div>
                                <div class="col-lg-9">
                                    <b-button variant="primary" @click="post_data()">
                                        Post &nbsp;&nbsp;<font-awesome-icon icon="upload"/>
                                    </b-button>
                                </div>
                                <div class="col-lg-9">
                                    <b-button variant="primary" @click="startTask()">
                                        Start Task &nbsp;&nbsp;<font-awesome-icon icon="upload"/>
                                    </b-button>
                                </div>
                            </div>
                            <div class="row row-grid justify-content-center align-items-center mt-lg">
                                <div class="col-lg-9">
                                    <base-progress :value="prg_val" :label="task_label"></base-progress>
                                </div>
                            </div>
                            <dl class="row">
                                <dt class="col-sm-3">Average Drive Time</dt>
                                <dd class="col-sm-9">
                                    <p class="text-muted">{{adt}}</p>
                                </dd>
                                <dt class="col-sm-3">Average Closest Location</dt>
                                <dd class="col-sm-9">
                                    <p class="text-muted">{{acl}}</p>
                                </dd>
                            </dl>
                            <div class="mt-5 row justify-content-center">
                                <div class="col-lg-9">
                                    <!--                                    <span>{{dta.intervals}}</span>-->
                                </div>
                            </div>
                            <b-button variant="primary" @click="toggleCharts()">
                                Toggle &nbsp;&nbsp;<font-awesome-icon icon="upload"/>
                            </b-button>
                            <div v-show="showCharts">
                                <!--                                <D3BarChart :key="componentKey"-->
                                <!--                                            class="d3-class"-->
                                <!--                                            :config="chart_config"-->
                                <!--                                            :datum="chart_data"-->
                                <!--                                            :title="chart_title"-->
                                <!--                                            :source="chart_source"-->
                                <!--                                ></D3BarChart>-->
                                <!--                                <D3BarChart :key="componentKey"-->
                                <!--                                            class="d3-class"-->
                                <!--                                            :config="chart_config"-->
                                <!--                                            :datum="chart_data_2"-->
                                <!--                                            :title="chart_title"-->
                                <!--                                            :source="chart_source"-->
                                <!--                                ></D3BarChart>-->
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
    import Papa from 'papaparse';
    import locationiq from "../api/locationiq";
    import restapi from "../api/restapi";
    import gmapsInit from '../plugins/gmaps';
    import {D3BarChart} from 'vue-d3-charts';
    import Tabs from "@/components/Tabs/Tabs.vue";
    import TabPane from "@/components/Tabs/TabPane.vue";
    import BaseProgress from "@/components/BaseProgress.vue";
    import {TabulatorComponent} from "vue-tabulator";
    import Charts from "./Charts";


    let tableData = [
        {id: 1, ad1: "", ad2: ""},
        {id: 2, ad1: "", ad2: ""},
        {id: 3, ad1: "", ad2: ""},
    ]


    let token = process.env.VUE_APP_LIQ_TOKEN


    export default {
        components: {
            D3BarChart,
            Tabs,
            TabPane,
            TabulatorComponent,
            BaseProgress
        },
        data() {
            return {
                prg_val: 0,
                task_label: "",
                total:100,
                componentKey: '',
                dta: '',
                adt: '',
                acl: '',
                ufile: null,
                file: '',
                text: '',
                showCharts: true,
                dReady: false,
                tdata: tableData,
                options: {
                    maxHeight: "1000px",
                    layout: "fitColumns",
                    clipboard: true,
                    clipboardPasteAction: "replace",
                    columns: [
                        {title: "Main Addresses", field: "ad1", widthGrow: 1},
                        {title: "Comparison Addresses", field: "ad2", widthGrow: 1}
                    ],
                },
                chart_title: 'Your title goes here',
                chart_source: 'Your source goes here',
                chart_data: [],
                chart_data_2: [],
                chart_config: {
                    key: 'range',
                    values: ['value'],
                    axis: {
                        yTicks: 3
                    },
                    color: {
                        default: '#222f3e',
                        current: '#41B882'
                    }
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

            async get_drivetime_data() {
                this.dta = await restapi.get_all_data(this.update_data)
            },

            update_data(data) {
                this.adt = data.mean_tot
                this.acl = data.min_loc_tot
                this.dta = data
                this.showCharts = true
                this.componentKey += 1;
                console.log(JSON.parse(this.dta.intervals))
                this.chart_data = this.convert_to_d3(JSON.parse(this.dta.intervals))
                this.chart_data_2 = this.convert_to_d3(JSON.parse(this.dta.cum_intervals))


            },
            convert_to_d3(data) {
                let workAsArray = []; // This will be the resulting array
                for (var key in data) {
                    var entry = {value: data[key], range: key}; // This will be each of the three graded things
                    // entry.id = key;
                    workAsArray.push(entry)
                }
                console.log(workAsArray)
                return workAsArray
            },
            async post_data() {
                const tabulatorInstance = this.$refs.tabulator.getInstance();
                this.tdata = tabulatorInstance.getData()
                this.dta = await restapi.dt_post(this.tdata, this.update_data)


                // console.log(tabulatorInstance.getData())
                // console.log(this.tdata)
            },
            toggleCharts() {
                this.showCharts = !this.showCharts
            },

            startTask() {
                restapi.start_test(this.update_progress)
            },

            update_progress(task_id) {
                this.polling = setInterval(() => {
                    restapi.update_status(task_id, this.set_update_prg)
                }, 1000)
            },

            set_update_prg(data) {
                if (data.state === 'FINISHED') {
                    clearInterval(this.polling)
                    this.task_label = "Task Complete"
                    this.prg_val = 100
                    this.update_data(data)
                } else if (data.state === 'PENDING') {
                    this.prg_val = 0
                    this.task_label = "Pending in Queue"
                } else {
                    if (this.task_label != "Task Running") {
                        this.task_label = "Task Running"
                        this.total = data.total
                    }
                    this.prg_val = parseInt((data.iter/this.total*100).toFixed(0))
                }
            },
        },
        beforeDestroy() {
            clearInterval(this.polling)
        },
        created() {
            vm.component = this
        }
        ,
    }
</script>
<style>
    .d3-class {
        display: block;
        height: 100%;
        width: 100%;
    }
</style>
