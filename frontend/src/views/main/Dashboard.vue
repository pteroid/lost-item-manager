<template>
  <v-container fluid>
    <search-form class="mb-4" @change="onSearchFormChange" />
    <v-row>
      <item-card
        class="mb-6"
        v-for="item in filteredItems"
        :key="item.id"
        :detail="item.detail"
        :kind="item.kind.name"
        :place="item.place.name"
        :pickedAt="item.picked_at"
        :imageUrl="item.image_url"
      />
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ItemCard from '@/components/ItemCard.vue';
import SearchForm from '../../components/SearchForm.vue';
import { readFilteredItems } from '@/store/main/getters';
import { Item } from '@/interfaces';

@Component({
  components: {
    ItemCard,
    SearchForm,
  },
})
export default class Dashboard extends Vue {
  public pickedAt: Date | null = null;
  public placeId: number | null = null;
  public kindId: number | null = null;

  get filteredItems(): Item[] {
    return readFilteredItems(this.$store)(
      this.pickedAt,
      this.placeId,
      this.kindId,
    );
  }

  public async onSearchFormChange(payload: {
    pickedAt: string | null;
    placeId: number | null;
    kindId: number | null;
  }) {
    if (payload.pickedAt) {
      this.pickedAt = new Date(payload.pickedAt);
    } else {
      this.pickedAt = null;
    }
    this.placeId = payload.placeId;
    this.kindId = payload.kindId;
  }
}
</script>
