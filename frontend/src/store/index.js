import Vue from 'vue'
import Vuex from 'vuex'
import fileManager from "./modules/fileManager"
import products from './modules/products'

Vue.use(Vuex);

export default new Vuex.Store({
  modules :{
    fileManager,
    products
  },
  strict: process.env.NODE_ENV !== 'production'
})