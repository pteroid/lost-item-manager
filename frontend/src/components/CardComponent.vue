<template>
  <v-card class="mx-4" max-width="300">
    <v-img height="160px" :src="imageUrl"></v-img>

    <v-card-title>{{ title }}</v-card-title>

    <v-card-subtitle>{{ pickedAt }}</v-card-subtitle>

    <v-card-text class="text--primary">
      <div>{{ describe }}</div>
    </v-card-text>

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

    <!-- <v-card-actions>
      <v-btn color="orange" text>Share</v-btn>

      <v-btn color="orange" text>Explore</v-btn>
    </v-card-actions>-->
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class CardComponent extends Vue {
  @Prop({ default: "" })
  title!: string;

  @Prop({ default: "" })
  describe!: string;

  @Prop({ default: "" })
  kind!: string;

  @Prop({ default: "" })
  place!: string;

  @Prop({ default: "" })
  pickedAt!: string;

  @Prop({ default: "" })
  imageUrl!: string;
}
</script>