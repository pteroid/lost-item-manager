<template>
  <v-container>
    <div class="mx-auto" style="max-width:400px">
      <h1 class="mt-4 pb-8">落とし物を追加</h1>
      <create-item></create-item>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import CreateItem from '@/components/CreateItem.vue';
import { readFilteredItems } from '@/store/main/getters';
import { Item } from '@/interfaces';

@Component({
  components: {
    CreateItem,
  },
})
export default class Dashboard extends Vue {}
</script>
