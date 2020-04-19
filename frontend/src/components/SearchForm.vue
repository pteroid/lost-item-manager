<template>
  <v-container>
    <v-expansion-panels popout>
      <v-expansion-panel>
        <v-expansion-panel-header>条件検索</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row>
            <v-col cols="12" md="6" lg="3">
              <v-select
                v-model="kindId"
                :items="kinds"
                item-text="name"
                item-value="id"
                label="種類"
                prepend-icon="mdi-format-list-bulleted-type"
                single-line
              ></v-select>
            </v-col>

            <v-col cols="12" md="6" lg="3">
              <v-select
                v-model="placeId"
                :items="places"
                item-text="name"
                item-value="id"
                label="場所"
                hide-details
                prepend-icon="mdi-access-point"
                single-line
              ></v-select>
            </v-col>

            <v-col cols="12" md="6" lg="3">
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
                    label="日付"
                    prepend-icon="event"
                    readonly
                    v-on="on"
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
            </v-col>

            <v-col cols="12" md="6" lg="3">
              <div>
                <v-btn color="error" @click="reset()">リセット</v-btn>
              </div>
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts">
import { Component, Emit, Watch, Vue } from 'vue-property-decorator';
import {readKinds, readPlaces} from '@/store/main/getters';

@Component
export default class SearchForm extends Vue {
  public kindId: number | null = null;
  public placeId: number | null = null;
  public pickedAt: string | null = null;
  public menu: boolean = false;

  get kinds() {
    return readKinds(this.$store);
  }

  get places() {
    return readPlaces(this.$store);
  }

  public reset() {
    this.kindId = null;
    this.placeId = null;
    this.pickedAt = null;
  }


  @Watch('kindId')
  @Watch('placeId')
  @Watch('pickedAt')
  @Emit()
  public change() {
    return {
      kindId: this.kindId,
      placeId: this.placeId,
      pickedAt: this.pickedAt,
    };
  }
}
</script>
