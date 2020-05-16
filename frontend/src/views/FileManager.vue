<template>
  <b-container>

    <br />

    <!-- PART-2: UPLOAD A FILE -->
    <b-card bg-variant="light">
      <b-form-file v-model="selFile"
                   ref="form"
                   placeholder="Drop a file here..."/>
      <b-button variant="primary" @click="submitFile()">
        Submit &nbsp; &nbsp;<font-awesome-icon icon="upload" /></b-button>
    </b-card>

    <br />

    <!-- PART-3: DELETE FILE(S) -->
    <b-card bg-variant="light">
      <b-row>
        <b-col><b-button variant="danger" @click="deleteFile()">
          Delete &nbsp;&nbsp;<font-awesome-icon icon="trash-alt" /></b-button>
        </b-col>
        <b-col md="auto">
          <b-card v-if="status">
            <b-card-text style="margin-right: 50px;">
              <strong>{{ selectedDataSizes.length }}</strong> File(s) selected</b-card-text>
            <b-card-text>Total size: <strong>{{ selectedDataTotal }}</strong></b-card-text>
          </b-card>
        </b-col>
      </b-row>

      <hr />

      <!-- PART-1: LIST FILES -->
      <ag-grid-vue style="width: 100%; height: 500px; border: 1px solid #e7e9ea; border-radius: 4px;"
                   class="ag-theme-material"
                   :row-height=60
                   :columnDefs="columnDefs"
                   :gridOptions="gridOptions"
                   :autoGroupColumnDef="autoGroupColumnDef"
                   :frameworkComponents="frameworkComponents"
                   :suppressRowClickSelection="true"
                   :groupSelectsChildren="true"
                   :debug="true"
                   :rowSelection="rowSelection"

                   :defaultColDef="{
                              sortable: true,
                              resizable: true,
                              filter: true
                              }"

                   :enableRangeSelection="true"
                   animateRows
                   @rowClicked = "onRowClicked"
                   @rowSelected = "onRowSelected"
                   :paginationAutoPageSize="true"
                   :pagination="true"
                   @gridReady="onGridReady"
                   :rowData="rowData">
      </ag-grid-vue>

  </b-card>

  <!-- PART-3: DELETE FILE(S) -->
  <!-- Modal Component -->
  <b-modal v-if="mShow" v-model="modal" @ok="handleOk" @cancel="$emit('close')">
      Selected file(s) will be deleted?
  </b-modal>

  </b-container>
</template>

<script>
import {AgGridVue} from "ag-grid-vue"
import filetypeCellRenderer from "../plugins/filetypeCellRenderer" // uploaded file type validator
import { mapState } from 'vuex'
import { sizeFormatter, dateFormatter } from '../plugins/utils' // Ag-grid display format for file size and date
export default {
  data () {
    return {
      selFile: null,
      columnDefs: null,
      autoGroupColumnDef: null,
      frameworkComponents: null,
      rowSelection: null,
      gridOptions: {},
      modal: false,
      mShow: false,
      result_id: null,
      status: false,
      selectedDataSizes: [],
      selectedDataTotal: 0
    }
  },
  components: {
      AgGridVue
  },
  beforeMount() {
    this.columnDefs = [
        {
          headerName: 'Name',
          field: 'name',
          width: 300,
          filterParams: { newRowsAction: "keep" },
          checkboxSelection: params => {
            return params.columnApi.getRowGroupColumns().length === 0;
          },
          headerCheckboxSelection: function(params) {
            return params.columnApi.getRowGroupColumns().length === 0;
          },
        },
        {
          headerName: 'Filetype',
          field: 'filetype',
          width: 80,
          cellRenderer: 'filetypeCellRenderer',
          filterParams: { newRowsAction: "keep" },
        },
        {
          headerName: 'Size',
          field: 'size',
          valueFormatter: sizeFormatter,
          width: 60,
          filterParams: { newRowsAction: "keep" }
        },
        {
          headerName: 'Added',
          field: 'since_added',
          width: 90,
          sort: 'desc',
          valueFormatter: dateFormatter
        }
    ]
    this.frameworkComponents = {
      filetypeCellRenderer: filetypeCellRenderer
    }
    this.autoGroupColumnDef = {
      headerName: "Group",
      width: 250,
      field: "name",
      valueGetter: params => {
        if (params.node.group) {
          return params.node.key;
        } else {
          return params.data[params.colDef.field];
        }
      },
      headerCheckboxSelection: true,
      cellRenderer: "agGroupCellRenderer",
      cellRendererParams: { checkbox: true }
    };
    this.rowSelection = "multiple";
  },
  mounted () {
    this.$store.dispatch('fileManager/loadFiles')
    this.gridOApi = this.gridOptions.api;
  },
    computed: mapState({
    rowData: state => state.fileManager.rowData
  }),
  methods: {
    onGridReady(params) {
      this.gridApi = params.api;
      this.columnApi = params.columnApi;
      params.api.sizeColumnsToFit();
      params.api.setRowData();
    },
    onRowSelected (event) {
      const selectedNodes = this.gridApi.getSelectedNodes();
      const selectedData = selectedNodes.map( node => node.data );
      const selectedDataStringPresentation = selectedData.map( node => node.name + ' ' + node.file_id).join(', ');
      this.selectedDataSizes = selectedData.map(node => node.size)
      // get the total size
      const add = (a, b) => a + b
      if (this.selectedDataSizes.length > 0) {
        this.status = true
        const totalSize = {value: this.selectedDataSizes.reduce(add)}
        this.selectedDataTotal = sizeFormatter(totalSize)
      } else { this.status = false }
    },
    submitFile () {
      if (this.selFile.size < 5 * 1024 * 1024) {
        var vm = this
        const fd = new FormData()
        fd.append('file', vm.selFile)
        this.$store.dispatch('fileManager/postFile', fd)
      } else {
        alert("File size must be smaller than 5MB")
      }
    },
    deleteFile () {
      const selectedNodes = this.gridApi.getSelectedNodes()
      if (selectedNodes.length > 0) {
        const selectedData = selectedNodes.map( node => node.data );
        const result_id = selectedData.map( node => node.file_id)
        console.log(result_id)
        this.result_id = result_id
        this.mShow = true
        this.modal = true
      }
    },
    handleOk () {
      this.$store.dispatch('fileManager/deleteFile', this.result_id)
      this.mShow = false
      this.status = false
    },
    onRowClicked(event) {
      let file_id = event.node.data.file_id
      let filename = event.node.data.name
      this.$store.dispatch('fileManager/downloadFile', filename)
    },
  }
}
</script>

<style lang="scss">

</style>