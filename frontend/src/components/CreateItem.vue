<template>
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
      class="mb-3"
      accept="image/*"
      label="画像"
      prepend-icon="mdi-file-image"
      :rules="[v => !!v || '画像を選択してください']"
      ref="file"
      @change="setImage"
    ></v-file-input>

    <img v-if="image_url" class="img-preview" :src="image_url" />

    <v-btn :disabled="!valid" color="success" large @click="submit">提出</v-btn>
  </v-form>
</template>


<script>
import { readKinds, readPlaces } from "@/store/main/getters";

export default {
  data: () => ({
    valid: true,
    detailRules: [
      v => !!v || "詳細を記述してください",
      v => (v && v.length <= 10) || "30文字以内で記述してください"
    ],
    image: null
  }),
  props: ["detail", "kind_id", "place_id", "image_url"],

  methods: {
    submit() {},
    setImage(e) {
      if (e === undefined) this.image_url = null;
      else this.image_url = window.URL.createObjectURL(e);
    }
  },

  mounted() {
    // ここで画像のURLをもとに画像ファイルをfile inputにセットするように加工
    if (this.image_url) {
    }
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

<style scoped>
.img-preview {
  width: 100%;
}
</style>
