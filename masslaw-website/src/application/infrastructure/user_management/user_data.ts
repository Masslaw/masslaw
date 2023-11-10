
export class MasslawUserData {
    public User_ID: string = '';
    public email: string = '';
    public first_name: string = '';
    public last_name: string = '';
    public phone: string = '';
    public cases: {
        owner: { case_id: string }[];
        participate: { case_id: string }[];
        viewer: { case_id: string }[];
        invited: { case_id: string, invite_type: string }[];
    } = {
        owner: [],
        participate: [],
        viewer: [],
        invited: []
    };
    public extra_data: {} = {};
}