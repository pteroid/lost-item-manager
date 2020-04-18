<template>
  <v-container fluid>
<!--    <v-card class="ma-3 pa-3">-->
<!--      <v-card-title primary-title>-->
<!--        <div class="headline primary&#45;&#45;text">Dashboard</div>-->
<!--      </v-card-title>-->
<!--      <v-card-text>-->
<!--        <div class="headline font-weight-light ma-5">Welcome {{greetedUser}}</div>-->
<!--      </v-card-text>-->
<!--      <v-card-actions>-->
<!--        <v-btn to="/main/profile/view">View Profile</v-btn>-->
<!--        <v-btn to="/main/profile/edit">Edit Profile</v-btn>-->
<!--        <v-btn to="/main/profile/password">Change Password</v-btn>-->
<!--      </v-card-actions>-->
<!--    </v-card>-->

<!--    <v-row :align="start" :justify="start">-->
<!--      <v-col v-for="n in 25" :key="n" cols="auto">-->
<!--        <v-card :elevation="n - 1" height="100" width="100">-->
<!--          <v-row class="fill-height" align="center" justify="center" v-text="n - 1"></v-row>-->
<!--        </v-card>-->
<!--      </v-col>-->
<!--    </v-row>-->
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';

@Component
export default class Dashboard extends Vue {
  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile && userProfile.full_name) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }
}
</script>
