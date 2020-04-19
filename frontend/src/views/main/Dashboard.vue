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
        :picked_at="item.picked_at"
        :image_url="item.image_url"
      />
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ItemCard from "@/components/ItemCard.vue";
import SearchForm from "../../components/SearchForm.vue";
import { readFilteredItems } from "@/store/main/getters";
import { Item } from "@/interfaces";

@Component({
  components: {
    ItemCard: ItemCard,
    SearchForm: SearchForm
  }
})
export default class Dashboard extends Vue {
  picked_at: Date | null = null;
  place_id: number | null = null;
  kind_id: number | null = null;

  get filteredItems(): Item[] {
    return readFilteredItems(this.$store)(
      this.picked_at,
      this.place_id,
      this.kind_id
    );
  }

  onSearchFormChange(payload: {
    picked_at: string | null;
    place_id: number | null;
    kind_id: number | null;
  }) {
    this.picked_at =
      ((payload.picked_at || null) as null) &&
      new Date(payload.picked_at as string);
    this.place_id = payload.place_id;
    this.kind_id = payload.kind_id;
  }
}
</script>
