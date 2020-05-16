<template>
  <ul>
    <li
      v-for="product in products"
      :key="product.id">
      {{ product.title }} - {{ product.price }}
      <br>
      <button
        :disabled="!product.inventory"
        @click="addToCart">
        Add to cart
      </button>
    </li>
  </ul>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  computed: mapState({
    products: state => state.products.all
  }),
  methods: {
      addToCart() {
          console.log("Added to cart ")
      }
  },
  created () {
    this.$store.dispatch('products/getAllProducts')
  }
}
</script>