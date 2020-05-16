/*!

=========================================================
* Vue Argon Design System - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-design-system
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-design-system/blob/master/LICENSE.md)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Vue from "vue";
import store from './store';
import App from "./App.vue";
import router from "./router";
import Argon from "./plugins/argon-kit";
import './registerServiceWorker';
import VueTabulator from 'vue-tabulator';
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VueTabulator);

// font awesome settings
import {library} from '@fortawesome/fontawesome-svg-core'
import {
    faFilePdf,
    faFileImage,
    faFileExcel,
    faFilePowerpoint,
    faFileWord,
    faFileVideo,
    faFileArchive,
    faFileAlt,
    faFile,
    faTrashAlt,
    faUpload,
    faTasks
} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

library.add(
    faFilePdf,
    faFileImage,
    faFileExcel,
    faFilePowerpoint,
    faFileWord,
    faFileVideo,
    faFileArchive,
    faFileAlt,
    faFile,
    faTrashAlt,
    faUpload,
    faTasks
)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false;
Vue.use(Argon);


window.vm = {}
new Vue({
    el: '#app',
    components: {
        'django': App
    },
    store,
    router,
    render: h => h(App)
}).$mount("#app");
