<template>
  <v-container>
    <div class="mx-auto" style="max-width:400px">
      <h1 class="mt-4 pb-8">落とし物を追加</h1>
      <v-form ref="form" v-model="valid">

        <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="290px"
        >
          <template v-slot:activator="{ on }">
            <v-text-field
                    v-model="pickedAt"
                    label="見つけた日"
                    prepend-icon="event"
                    readonly
                    v-on="on"
                    :rules="[v => !!v || '日付を選択してください']"
            ></v-text-field>
          </template>
          <v-date-picker
                  v-model="pickedAt"
                  locale="jp-ja"
                  no-title
                  scrollable
                  :day-format="date => new Date(date).getDate()"
                  @change="menu = false"
          >
          </v-date-picker>
        </v-menu>

        <v-select
                v-model="placeId"
                :items="places"
                item-text="name"
                item-value="id"
                :rules="[v => !!v || '場所を選択してださい']"
                label="見つけた場所"
                prepend-icon="place"
                required
        ></v-select>

        <v-select
                v-model="kindId"
                :items="kinds"
                item-text="name"
                item-value="id"
                :rules="[v => !!v || '種類を選択してください']"
                label="種類"
                prepend-icon="mdi-format-list-bulleted-type"
                required
        ></v-select>

        <v-text-field
                v-model="detail"
                :counter="30"
                :rules="[ v => (!v || v.length <= 10) || '30文字以内で記述してください']"
                label="詳細"
                prepend-icon="image_search"
        ></v-text-field>

        <v-file-input
                class="mb-3"
                accept="image/*"
                label="画像"
                prepend-icon="image"
                ref="file"
                @change="setImage"
        ></v-file-input>

        <img v-if="imageUrl" class="img-preview" :src="imageUrl"  alt="lost item"/>


        <v-btn class="mr-4" :disabled="!valid" color="success" large @click="doSubmit">提出</v-btn>
        <v-btn class="mr-4" color="normal" large @click="doBack">キャンセル</v-btn>

      </v-form>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {dispatchCheckLoggedIn, dispatchCreateItem} from '@/store/main/actions';
import { readKinds, readPlaces } from '@/store/main/getters';
import store from '@/store';
import { ItemCreate } from '@/backend';
import { getDateString } from '@/utils';


const createRouteGuard = async (to, from, next) => {
  if (dispatchCheckLoggedIn(store)) {
    next();
  } else {
    next('/');
  }
};


@Component
export default class Create extends Vue {
  public valid: boolean = true;
  public menu: boolean = false;
  public pickedAt: string = getDateString(new Date());
  public placeId: number | null = null;
  public kindId: number | null = null;
  public detail: string | null = null;
  public imageFile: File | null = null;
  public imageUrl: string | null = null;

  public setImage(file: File) {
    if (file) {
      this.imageFile = file;
      this.imageUrl = URL.createObjectURL(file);
    } else {
      this.imageFile = null;
      this.imageUrl = null;
    }
  }

  public async doSubmit() {
    if (this.placeId === null || this.kindId === null) { return; }

    const uploadItem: ItemCreate = {
      place_id: this.placeId,
      kind_id: this.kindId,
      picked_at: this.pickedAt,
      detail: this.detail || undefined,
    };

    await dispatchCreateItem(this.$store, {
      item: uploadItem,
      imageFile: this.imageFile || undefined,
    });

    this.$router.back();
  }

  public doBack() {
    this.$router.back();
  }


  get kinds() {
    return readKinds(this.$store);
  }
  get places() {
    return readPlaces(this.$store);
  }


  public beforeRouteEnter(to, from, next) {
    createRouteGuard(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    createRouteGuard(to, from, next);
  }
}
</script>

<style scoped>
  .img-preview {
    width: 100%;
  }
</style>
