import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { MainState } from './state';

const defaultState: MainState = {
  isLoggedIn: null,
  token: '',
  logInError: false,
  admin: null,
  dashboardMiniDrawer: false,
  dashboardShowDrawer: true,
  notifications: [],
  items: [],
  places: [],
  kinds: [],
};

export const mainModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
