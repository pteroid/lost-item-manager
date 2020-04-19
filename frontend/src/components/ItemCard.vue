<template>
  <v-card class="mx-4" max-width="300">
    <v-img height="160px" :src="imageUrl || ''"></v-img>

    <v-card-text class="text--primary pb-1 mb-0">
      <div>{{ detail }}</div>
    </v-card-text>

    <v-card-subtitle>{{ pickedAt }}</v-card-subtitle>

    <v-divider class="mx-4"></v-divider>

    <v-card-text>
      <v-chip class="mr-2">
        <v-icon left>mdi-format-list-bulleted-type</v-icon>
        {{ kind }}
      </v-chip>
      <v-chip class="mr-2">
        <v-icon left>mdi-access-point</v-icon>
        {{ place }}
      </v-chip>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class ItemCard extends Vue {
  @Prop({ default: '' })
  public detail!: string;

  @Prop({ default: '' })
  public kind!: string;

  @Prop({ default: '' })
  public place!: string;

  @Prop({ default: '' })
  public pickedAt!: string;

  @Prop({ default: null })
  public imageUrl!: string | null;
}
</script>
