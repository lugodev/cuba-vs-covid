<template>
  <div>
    <nav class="breadcrumb" aria-label="breadcrumbs">
      <ul>
        <li><nuxt-link to="/dashboard/products">Productos</nuxt-link></li>
        <li class="is-active">
          <a href="#" aria-current="page">Añadir producto</a>
        </li>
      </ul>
    </nav>
    <form @submit.stop.prevent="add()">
      <!-- stlmodel -->
      <label for="" class="label">Modelo</label>
      <b-field>
        <b-select
          v-model="$v.form.stlmodel.$model"
          placeholder="Selecciona un modelo"
          expanded
        >
          <option
            v-for="stlmodel in stlmodels"
            :key="stlmodel.id"
            :value="stlmodel.id"
          >
            {{ stlmodel.name }}
          </option>
        </b-select>
      </b-field>
      <!-- end stlmodel -->

      <!-- phone -->
      <label for="" class="label">Cantidad en inventario</label>
      <b-field>
        <b-input v-model="$v.form.stock.$model"></b-input>
      </b-field>
      <!-- end phone -->

      <b-field>
        <b-button
          type="is-primary"
          native-type="submit"
          :loading="form.loading"
          :disabled="$v.form.$invalid"
        >
          Añadir producto
        </b-button>
      </b-field>
    </form>
  </div>
</template>

<script>
import gql from 'graphql-tag'
import { required, integer } from 'vuelidate/lib/validators'
export default {
  layout: 'dashboard',
  data() {
    return {
      stlmodels: [],
      form: {
        stlmodel: null,
        stock: null
      }
    }
  },
  validations: {
    form: {
      stlmodel: {
        required
      },
      stock: {
        required,
        integer
      }
    }
  },
  mounted() {
    this.$apollo
      .query({
        query: gql`
          query stlmodels {
            stlmodels {
              id
              name
            }
          }
        `
      })
      .then(({ data }) => {
        this.stlmodels = data.stlmodels
      })
  },
  methods: {
    add() {
      this.$v.form.$touch()
      if (!this.$v.form.$invalid) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation createProduct($stlmodel: String!, $stock: Int!) {
                createProduct(stlmodel: $stlmodel, stock: $stock) {
                  status
                }
              }
            `,
            variables: {
              stlmodel: this.form.stlmodel,
              stock: this.form.stock
            }
          })
          .then(({ data }) => {
            if (data.createProduct.status === 'ok') {
              this.$buefy.toast.open('Se añadió el producto')
              this.$router.replace('/dashboard/products')
            }
          })
      }
    }
  }
}
</script>

<style scoped></style>
