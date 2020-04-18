import { api } from '@/api';
import router from '@/router';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import {
    commitAddNotification,
    commitRemoveNotification,
    commitSetLoggedIn,
    commitSetLogInError,
    commitSetToken,
    commitSetAdmin,
    commitSetItems,
    commitSetPlaces,
    commitSetKinds,
} from './mutations';
import { AppNotification, MainState } from './state';

import * as backend from '@/backend';

type MainContext = ActionContext<MainState, State>;


export const actions = {
    async actionLogIn(context: MainContext, payload: { username: string; password: string }) {
        try {
            const client = new backend.LoginApi();
            const response = await client.
                  loginAccessTokenApiV1LoginAccessTokenPost(payload.username, payload.password);
            const token = response.data.access_token;
            if (token) {
                saveLocalToken(token);
                commitSetToken(context, token);
                commitSetLoggedIn(context, true);
                commitSetLogInError(context, false);
                await dispatchGetUserProfile(context);
                await dispatchRouteLoggedIn(context);
                commitAddNotification(context, { content: 'Logged in', color: 'success' });
            } else {
                await dispatchLogOut(context);
            }
        } catch (err) {
            commitSetLogInError(context, true);
            await dispatchLogOut(context);
        }
    },
    async actionGetUserProfile(context: MainContext) {
        try {
            // const response = await api.getMe(context.state.token);
            const client = new backend.AdminsApi({accessToken: context.state.token});
            const response = await client.readCurrentAdminApiV1AdminsMeGet();
            if (response.data) {
                commitSetAdmin(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateUserProfile(context: MainContext, payload) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const client = new backend.AdminsApi({accessToken: context.state.token});
            const response = (await Promise.all([
                // api.updateMe(context.state.token, payload),
                client.updateCurrentAdminApiV1AdminsMePut(payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetAdmin(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Profile successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCheckLoggedIn(context: MainContext) {
        if (!context.state.isLoggedIn) {
            let token = context.state.token;
            if (!token) {
                const localToken = getLocalToken();
                if (localToken) {
                    commitSetToken(context, localToken);
                    token = localToken;
                }
            }
            if (token) {
                try {
                    const client = new backend.AdminsApi({accessToken: token});
                    // const response = await api.getMe(token);
                    const response = await client.readCurrentAdminApiV1AdminsMeGet();

                    commitSetLoggedIn(context, true);
                    commitSetAdmin(context, response.data);
                } catch (error) {
                    await dispatchRemoveLogIn(context);
                }
            } else {
                await dispatchRemoveLogIn(context);
            }
        }
    },
    async actionRemoveLogIn(context: MainContext) {
        removeLocalToken();
        commitSetToken(context, '');
        commitSetLoggedIn(context, false);
    },
    async actionLogOut(context: MainContext) {
        await dispatchRemoveLogIn(context);
        await dispatchRouteLogOut(context);
    },
    async actionUserLogOut(context: MainContext) {
        await dispatchLogOut(context);
        commitAddNotification(context, { content: 'Logged out', color: 'success' });
    },
    actionRouteLogOut(context: MainContext) {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    },
    async actionCheckApiError(context: MainContext, payload: AxiosError) {
        if (payload.response!.status === 401) {
            await dispatchLogOut(context);
        }
    },
    actionRouteLoggedIn(context: MainContext) {
        if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
            router.push('/main');
        }
    },
    async removeNotification(context: MainContext, payload: { notification: AppNotification, timeout: number }) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                commitRemoveNotification(context, payload.notification);
                resolve(true);
            }, payload.timeout);
        });
    },
    async passwordRecovery(context: MainContext, payload: { username: string }) {
        const loadingNotification = { content: 'Sending password recovery email', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const client = new backend.LoginApi();
            const response = (await Promise.all([
                // api.passwordRecovery(payload.username),
                client.recoverPasswordApiV1PasswordRecoveryEmailPost(payload.username),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Password recovery email sent', color: 'success' });
            await dispatchLogOut(context);
        } catch (error) {
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { color: 'error', content: 'Incorrect username' });
        }
    },
    async resetPassword(context: MainContext, payload: { password: string, token: string }) {
        const loadingNotification = { content: 'Resetting password', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const client = new backend.LoginApi();
            const response = (await Promise.all([
                // api.resetPassword(payload.password, payload.token),
                client.resetPasswordApiV1ResetPasswordPost({
                  new_password: payload.password,
                  token: payload.token,
                }),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Password successfully reset', color: 'success' });
            await dispatchLogOut(context);
        } catch (error) {
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { color: 'error', content: 'Error resetting password' });
        }
    },
    async getItems(context: MainContext) {
        try {
            const client = new backend.ItemsApi();
            const response = await client.readItemsApiV1ItemsGet();
            if (response.data) {
                commitSetItems(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },

    async getPlaces(context: MainContext) {
        try {
            const client = new backend.PlacesApi();
            const response = await client.readPlacesApiV1PlacesGet();
            if (response.data) {
                commitSetPlaces(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async getKinds(context: MainContext) {
        try {
            const client = new backend.PlacesApi();
            const response = await client.readPlacesApiV1PlacesGet();
            if (response.data) {
                commitSetKinds(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },

};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchUpdateUserProfile = dispatch(actions.actionUpdateUserProfile);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchPasswordRecovery = dispatch(actions.passwordRecovery);
export const dispatchResetPassword = dispatch(actions.resetPassword);
export const dispatchGetItems = dispatch(actions.getItems);
export const dispatchGetPlaces = dispatch(actions.getPlaces);
export const dispatchGetKinds = dispatch(actions.getKinds);
