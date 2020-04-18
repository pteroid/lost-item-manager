<template>
  <router-view></router-view>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { store } from "@/store";
import {
  dispatchCheckLoggedIn,
  dispatchGetItems,
  dispatchGetPlaces,
  dispatchGetKinds
} from "@/store/main/actions";
import { readIsLoggedIn } from "@/store/main/getters";

const startRouteGuard = async (to, from, next) => {
  await dispatchCheckLoggedIn(store);
  await dispatchGetPlaces(store);
  await dispatchGetKinds(store);
  await dispatchGetItems(store);

  if (to.path === "/login" || to.path === "/") {
    next("/main");
  } else {
    next();
  }
};

@Component
export default class Start extends Vue {
  public beforeRouteEnter(to, from, next) {
    startRouteGuard(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    startRouteGuard(to, from, next);
  }
}
</script>
