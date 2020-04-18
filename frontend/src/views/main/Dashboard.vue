<template>
  <v-container fluid>
    <filter-component />
    <card-component
      v-for="(item, i) in items"
      :key="i"
      :describe="item.describe"
      :kind="item.kind"
      :place="item.place"
      :pickedAt="item.pickedAt"
      :imageUrl="item.imageUrl"
    />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
// import { readUserProfile } from "@/store/main/getters";
import CardComponent from "../../components/CardComponent";
import FilterComponent from "../../components/FilterComponent";

@Component({
  components: {
    CardComponent,
    FilterComponent
  }
})
export default class Dashboard extends Vue {
  // get greetedUser() {
  //   const userProfile = readUserProfile(this.$store);
  //   if (userProfile && userProfile.full_name) {
  //     if (userProfile.full_name) {
  //       return userProfile.full_name;
  //     } else {
  //       return userProfile.email;
  //     }
  //   }
  // }

  get items() {
    const items = this.$store.getters.items;
    for (var i = 0; i < items.length; i++) {
      console.log(items[i]);
    }
    return [
      {
        title: "1111",
        describe: "1111111",
        kind: "234",
        place: "234",
        pickedAt: "2022-10-4",
        imageUrl:
          "https://hyodoblog.com/wp-content/uploads/2020/01/rails-devise-sendgrid.jpg"
      }
    ];
  }
}
</script>
