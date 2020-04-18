<template>
  <v-container>
    <v-expansion-panels popout>
      <v-expansion-panel>
        <v-expansion-panel-header>条件検索</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row>
            <v-col cols="12" md="6" lg="3">
              <v-select
                v-model="kind"
                :items="kinds"
                menu-props="auto"
                label="種類"
                prepend-icon="mdi-format-list-bulleted-type"
                single-line
              ></v-select>
            </v-col>

            <v-col cols="12" md="6" lg="3">
              <v-select
                v-model="place"
                :items="places"
                menu-props="auto"
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
                :return-value.sync="pickedAt"
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
                <v-date-picker v-model="pickedAt" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu.save(pickedAt)">OK</v-btn>
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
import { Component, Emit, Vue } from "vue-property-decorator";

@Component
export default class FilterComponent extends Vue {
  kind: string = "";
  place: string = "";
  pickedAt: string = "";
  menu: boolean = false;

  get kinds() {
    const kinds = this.$store.getters.kinds;
    var array = [];
    for (var i = 0; i < kinds.length; i++) {
      array.push(kinds[i].name);
    }
    return array;
  }

  get places() {
    const places = this.$store.getters.places;
    var array = [];
    for (var i = 0; i < places.length; i++) {
      array.push(places[i].name);
    }
    return array;
  }

  @Emit("reset")
  reset() {
    this.kind = "";
    this.place = "";
    this.pickedAt = "";
  }
}
</script>
