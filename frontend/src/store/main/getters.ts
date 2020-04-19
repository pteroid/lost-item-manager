import { MainState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    hasAdminAccess: (state: MainState) => {
        return (
            state.admin && state.admin.is_active);
    },
    loginError: (state: MainState) => state.logInError,
    dashboardShowDrawer: (state: MainState) => state.dashboardShowDrawer,
    dashboardMiniDrawer: (state: MainState) => state.dashboardMiniDrawer,
    userProfile: (state: MainState) => state.admin,
    token: (state: MainState) => state.token,
    isLoggedIn: (state: MainState) => state.isLoggedIn,
    firstNotification: (state: MainState) => state.notifications.length > 0 && state.notifications[0],
    items: (state: MainState) => state.items,
    places: (state: MainState) => state.places,
    kinds: (state: MainState) => state.kinds,
    filteredItems: (state: MainState) =>
      (pickedAt: Date | null, placeId: number | null, kindId: number | null) =>
        state.items.filter((item) => (
          (!pickedAt || item.picked_at_date.getTime() === pickedAt.getTime()) &&
          (!placeId || item.place_id === placeId) &&
          (!kindId || item.kind_id === kindId)
        ))
    ,
};

const {read} = getStoreAccessors<MainState, State>('');

export const readDashboardMiniDrawer = read(getters.dashboardMiniDrawer);
export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readHasAdminAccess = read(getters.hasAdminAccess);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);
export const readItems = read(getters.items);
export const readPlaces = read(getters.places);
export const readKinds = read(getters.kinds);
export const readFilteredItems = read(getters.filteredItems);
