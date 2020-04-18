import {Item} from '@/interfaces';
import {Admin, Place, Kind} from '@/backend';

export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
}


export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: boolean;
    admin: Admin | null;
    dashboardMiniDrawer: boolean;
    dashboardShowDrawer: boolean;
    notifications: AppNotification[];
    items: Item[];
    places: Place[];
    kinds: Kind[];
}
