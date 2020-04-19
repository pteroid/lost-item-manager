<template>
  <v-app class="mx-auto" style="max-width:400px">
    <h1 class="mx-4 pb-4">落とし物を追加</h1>
    <v-form ref="form" v-model="valid">
      <v-text-field v-model="detail" :counter="30" :rules="detailRules" label="詳細" required></v-text-field>

      <v-select
        v-model="kind_id"
        :items="kinds"
        item-text="name"
        item-value="id"
        :rules="[v => !!v || '種類を選択してください']"
        label="種類"
        prepend-icon="mdi-format-list-bulleted-type"
        required
      ></v-select>

      <v-select
        v-model="place_id"
        :items="places"
        item-text="name"
        item-value="id"
        :rules="[v => !!v || '場所を選択してださい']"
        label="見つけた場所"
        prepend-icon="mdi-access-point"
        required
      ></v-select>

      <v-file-input
        accept="image/*"
        label="画像"
        prepend-icon="mdi-file-image"
        :rules="[v => !!v || '画像を選択してください']"
      ></v-file-input>

      <v-btn :disabled="!valid" color="success" large @click="submit">提出</v-btn>
    </v-form>
  </v-app>
</template>


<script>
import { readKinds, readPlaces } from "@/store/main/getters";

export default {
  data: () => ({
    valid: true,
    detail: "",
    detailRules: [
      v => !!v || "詳細を記述してください",
      v => (v && v.length <= 10) || "30文字以内で記述してください"
    ],
    kind_id: null,
    place_id: null
  }),

  methods: {
    submit() {}
  },

  computed: {
    kinds() {
      return readKinds(this.$store);
    },
    places() {
      return readPlaces(this.$store);
    }
  }
};
</script>