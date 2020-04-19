<template>
  <v-container>
    <create-item></create-item>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import CreateItem from "@/components/CreateItem.vue";
import { readFilteredItems } from "@/store/main/getters";
import { Item } from "@/interfaces";

@Component({
  components: {
    CreateItem: CreateItem
  }
})
export default class Dashboard extends Vue {}
</script>
