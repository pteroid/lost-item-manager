import { IUserProfile } from '@/interfaces';
import { MainState, AppNotification } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import {Admin, Kind, Place} from '@/backend';
import  {Item} from '@/interfaces';
import * as backend from '@/backend';


export const mutations = {
    setToken(state: MainState, payload: string) {
        state.token = payload;
    },
    setLoggedIn(state: MainState, payload: boolean) {
        state.isLoggedIn = payload;
    },
    setLogInError(state: MainState, payload: boolean) {
        state.logInError = payload;
    },
    setUserProfile(state: MainState, payload: Admin) {
        state.admin = payload;
    },
    setDashboardMiniDrawer(state: MainState, payload: boolean) {
        state.dashboardMiniDrawer = payload;
    },
    setDashboardShowDrawer(state: MainState, payload: boolean) {
        state.dashboardShowDrawer = payload;
    },
    addNotification(state: MainState, payload: AppNotification) {
        state.notifications.push(payload);
    },
    removeNotification(state: MainState, payload: AppNotification) {
        state.notifications = state.notifications.filter((notification) => notification !== payload);
    },
    setItems(state: MainState, payload: backend.Item[]) {
        state.items = payload.map((item) => {
          return {...item,
              place: state.places.find(({id}) => id === item.place_id),
              kind: state.kinds.find(({id}) => id === item.kind_id),
          } as Item;
        });
    },
    setPlaces(state: MainState, payload: Place[]) {
        state.places = payload;
    },
    setKinds(state: MainState, payload: Kind[]) {
        state.kinds = payload;
    },
};

const {commit} = getStoreAccessors<MainState | any, State>('');

export const commitSetDashboardMiniDrawer = commit(mutations.setDashboardMiniDrawer);
export const commitSetDashboardShowDrawer = commit(mutations.setDashboardShowDrawer);
export const commitSetLoggedIn = commit(mutations.setLoggedIn);
export const commitSetLogInError = commit(mutations.setLogInError);
export const commitSetToken = commit(mutations.setToken);
export const commitSetAdmin = commit(mutations.setUserProfile);
export const commitAddNotification = commit(mutations.addNotification);
export const commitRemoveNotification = commit(mutations.removeNotification);
export const commitSetItems = commit(mutations.setItems);
export const commitSetPlaces = commit(mutations.setPlaces);
export const commitSetKinds = commit(mutations.setKinds);
