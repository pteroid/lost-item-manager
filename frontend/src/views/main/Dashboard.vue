<template>
  <v-container fluid>
    <card-component
      v-for="(item, i) in items"
      :key="i"
      :title="item.title"
      :describe="item.describe"
      :kind="item.kind"
      :place="item.place"
      :pickedAt="item.pickedAt"
      :imageUrl="item.imageUrl"
    ></card-component>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
// import { readUserProfile } from "@/store/main/getters";
import CardComponent from "../../components/CardComponent";

@Component({
  components: {
    CardComponent
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
