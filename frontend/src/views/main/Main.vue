<template>
  <div>
    <v-app-bar dark color="primary" app>
      <v-toolbar-title v-text="appName"></v-toolbar-title>
      <v-spacer></v-spacer>
      <router-link to="/main/create" v-if="isLoggedIn">
        <v-btn icon>
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </router-link>
      <v-menu bottom left offset-y>
        <template #activator="{ on }">
          <v-btn v-on="on" icon>
            <v-icon>more_vert</v-icon>
          </v-btn>
        </template>
        <v-list v-if="isLoggedIn">
          <v-list-item to="/main/create">
            <v-list-item-content>
              <v-list-item-title>追加</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon>add</v-icon>
            </v-list-item-action>
          </v-list-item>
          <v-list-item @click="logout">
            <v-list-item-content>
              <v-list-item-title>ログアウト</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon>close</v-icon>
            </v-list-item-action>
          </v-list-item>
        </v-list>
        <v-list v-else>
          <v-list-item to="/login">
            <v-list-item-content>
              <v-list-item-title>ログイン</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon>account_circle</v-icon>
            </v-list-item-action>
          </v-list-item>
        </v-list>



      </v-menu>
    </v-app-bar>
    <v-content>
      <router-view></router-view>
    </v-content>
    <v-footer class="pa-3" fixed app>
      <v-spacer></v-spacer>
      <span>&copy; {{appName}}</span>
    </v-footer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

import { appName } from '@/env';
import {
  readIsLoggedIn,
} from '@/store/main/getters';
import { dispatchUserLogOut } from '@/store/main/actions';

const routeGuardMain = async (to, from, next) => {
  if (to.path === '/main') {
    next('/main/dashboard');
  } else {
    next();
  }
};

@Component
export default class Main extends Vue {
  public appName = appName;

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  get isLoggedIn() {
    return readIsLoggedIn(this.$store);
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }
}
</script>
