<template>
    <div class="profile-page">
        <section class="section-profile-cover section-shaped my-0">
            <div class="shape shape-style-1 shape-dark shape-skew alpha-4">
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
                            <tabs ref="tabs" tabNavClasses="nav-fill flex-column flex-sm-row nav-wrapper"
                                  tabContentClasses="card shadow">
                                <tab-pane id="upload">
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
                                        <div class="mt-3 px-5 row justify-content-center">
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
                                    <div class="mt-2 mb-5 row justify-content-center">
                                        <div class="col-lg-9">
                                            <b-button variant="primary" @click="submitFile()">
                                                Import Address List &nbsp;&nbsp;<font-awesome-icon icon="upload"/>
                                            </b-button>
                                        </div>
                                    </div>
                                    <div v-show="showUpTable" class="mt-2 ml-2 mr-2 py-1 row justify-content-end">
                                        <b-button variant="secondary" @click="delete_row()">
                                            Delete Row &nbsp;&nbsp;<font-awesome-icon icon="trash-alt"/>
                                        </b-button>
                                    </div>
                                    <div v-show="showUpTable" class="ml-2 mr-2 py-5 row justify-content-center">
                                        <VueTabulator ref="tabulatorup" v-model="tdataup" :options="optionsUp"
                                                      :integration="{ updateStrategy: 'REPLACE`' }"/>

                                    </div>
                                </tab-pane>
                                <tab-pane id="paste">
                                <span slot="title">
                                    <i class="ni ni-bell-55 "></i>
                                    Paste Data From Excel/CSV File
                                </span>
                                    <div class="mt-2 ml-2 mr-2 px-2 py-3 row">
                                        <h3 class="heading-title text-warning mb-1">Data Clipboard</h3>
                                        <p class="text-left">Paste pairs of longitude and latitude data into the
                                            respective columns to perform matrix distance analysis...</p>
                                    </div>
                                    <div class="mt-1 ml-2 mr-2 row justify-content-center">
                                        <VueTabulator ref="tabulator" v-model="tdata" :options="options"
                                                      :integration="{ updateStrategy: 'REPLACE`' }"/>
                                    </div>
                                </tab-pane>
                            </tabs>
                            <div class="mt-5 row justify-content-center">
                                <div v-show="showTask" class="col-lg-9">
                                    <b-button variant="primary" @click="startTask()">
                                        Start Task &nbsp;&nbsp;<font-awesome-icon icon="upload"/>
                                    </b-button>
                                </div>

                            </div>
                            <div v-show="!showTask" class="row row-grid justify-content-center align-items-center">
                                <div class="col-lg-9">
                                    <base-progress :value="prg_val" :label="task_label"></base-progress>
                                </div>
                            </div>
                            <div v-show="showCharts">
                                <div class="row justify-content-center">
                                    <div class="col-lg-4 order-lg-1">
                                        <div class="card-profile-stats d-flex justify-content-center">
                                            <div>
                                                <span class="heading">{{convertMinsToHrsMins(adt)}}</span>
                                                <span class="description">Average Drive Time</span>
                                            </div>
                                            <div>
                                                <span class="heading">{{convertMinsToHrsMins(acl)}}</span>
                                                <span class="description">Average Closest Location</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <D3BarChart :key="componentKey"
                                            class="d3-class"
                                            :config="chart_config"
                                            :datum="chart_data"
                                            :title="chart_title"
                                            :source="chart_source"
                                ></D3BarChart>
                                <D3BarChart :key="componentKey_2"
                                            class="d3-class"
                                            :config="chart_config"
                                            :datum="chart_data_2"
                                            :title="chart_title_2"
                                            :source="chart_source"
                                ></D3BarChart>
                                <div class="row justify-content-center">
                                    <base-button v-show="dReady" type="primary" @click="download()">Download Results
                                    </base-button>
                                </div>
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
    import restapi from "../api/restapi";
    import {D3BarChart} from 'vue-d3-charts';
    import Tabs from "@/components/Tabs/Tabs.vue";
    import TabPane from "@/components/Tabs/TabPane.vue";
    import BaseProgress from "@/components/BaseProgress.vue";
    import {TabulatorComponent} from "vue-tabulator";


    let tableData = [
        {id: 1, ad1: "", ad2: ""},
        {id: 2, ad1: "", ad2: ""},
        {id: 3, ad1: "", ad2: ""},
    ]

    let tableDataUp = tableData


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
                task_label: "Task Pending",
                total: 100,
                componentKey: 1,
                componentKey_2: this.componentKey,
                dta: '',
                adt: '',
                acl: '',
                ufile: null,
                file: '',
                text: '',
                showCharts: false,
                showUpTable: false,
                dReady: true,
                showTask: true,
                tdata: tableData,
                tdataup: tableDataUp,
                fileData: null,
                optionsUp: {
                    selectable: true,
                    maxHeight: "1000px",
                    layout: "fitColumns",
                    clipboard: true,
                    clipboardPasteAction: "replace",
                    columns: [
                        {title: "Main Addresses", field: "ad1", widthGrow: 1},
                        {title: "Comparison Addresses", field: "ad2", widthGrow: 1}
                    ],
                },
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
                chart_title: 'Number of locations within a range of x-x minutes',
                chart_title_2: 'Cumulative number of locations within a range of x-x minutes',
                chart_source: 'Range (Mins)',
                chart_data: [],
                chart_data_2: [],
                chart_config: {
                    key: 'range',
                    values: ['value'],
                    axis: {
                        yTicks: 3
                    },
                    color: {
                        current: '#172b4d',
                        default: '#17a2b8'
                    }
                }
            }
        },
        methods: {
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
            convertToTable(data) {
                let newTableData = [];
                for (let i = 0; i < data.length; i++) {
                    if (data[i][0] !== "") {
                        newTableData.push({id: this.tdataup.length, ad1: data[i][0], ad2: data[i][1]});
                    }
                }
                this.tdataup = newTableData;
                this.toggleUpData();

            },
            printData(data) {
                console.log(data)
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
            convertMinsToHrsMins(mins) {
                let h = Math.floor(mins / 60);
                let m = Math.floor(mins) % 60;
                h = h < 10 ? '0' + h : h;
                m = m < 10 ? '0' + m : m;
                return `${h}:${m}`;
            },

            download() {
                let csv = Papa.unparse(this.fileData)
                console.log(csv)
                let filename = "drive_time_results.csv";
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
            async get_drivetime_data() {
                this.dta = await restapi.get_all_data(this.update_data)
            },
            update_data(data) {
                this.adt = data.mean_tot
                this.acl = data.min_loc_tot
                this.dta = data
                this.showCharts = true
                this.componentKey += 1;
                this.componentKey_2 += 1;
                this.fileData = JSON.parse(data.data)
                console.log(this.fileData)
                let newData = []
                for (let key in this.fileData) {
                    const newRow = {...this.fileData[key], location: key,}
                    newData.push(newRow)
                }
                this.fileData = newData
                this.chart_data = this.convert_to_d3(JSON.parse(this.dta.intervals))
                this.chart_data_2 = this.convert_to_d3(JSON.parse(this.dta.cum_intervals))

            }
            ,
            convert_to_d3(data) {
                let workAsArray = []; // This will be the resulting array
                for (var key in data) {
                    var entry = {value: data[key], range: key}; // This will be each of the three graded things
                    workAsArray.push(entry)
                }
                return workAsArray
            }
            ,

            async post_data() {
                const tabulatorInstance = this.$refs.tabulator.getInstance();
                this.tdata = tabulatorInstance.getData()
                this.dta = await restapi.dt_post(this.tdata, this.update_data)
            }
            ,
            toggleTask() {
                this.showTask = !this.showTask
            }
            ,

            toggleUpData() {
                this.showUpTable = true
            }
            ,

            startTask() {
                const tabs = this.$refs.tabs;
                const acttab = tabs.activeTabIndex;
                this.toggleTask()
                if (acttab == 0){
                    const tabledata = this.tdataup
                    restapi.start_task(tabledata, this.update_progress)
                } else {
                    const tabulatorInstance = this.$refs.tabulator.getInstance();
                    const tabledata = tabulatorInstance.getData()
                    restapi.start_task(tabledata, this.update_progress)
                }
            }
            ,

            update_progress(task_id) {
                this.polling = setInterval(() => {
                    restapi.update_status(task_id, this.set_update_prg)
                }, 1000)
            }
            ,

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
                    this.prg_val = parseInt((data.iter / this.total * 100).toFixed(0))
                }
            }
            ,
            delete_row() {
                const tabulatorInstance = this.$refs.tabulatorup.getInstance();
                const selectedRows = tabulatorInstance.getSelectedRows(); //get array of currently selected row components.
                selectedRows.forEach(element =>
                    element.delete()
                );
                this.tdataup = tabulatorInstance.getData()

            },
        },
        beforeDestroy() {
            clearInterval(this.polling)
        }
        ,
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
