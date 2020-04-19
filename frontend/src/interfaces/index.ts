import * as backend from '@/backend';

export interface Item extends backend.Item {
    picked_at_date: Date;
    place: backend.Place;
    kind: backend.Kind;
}
