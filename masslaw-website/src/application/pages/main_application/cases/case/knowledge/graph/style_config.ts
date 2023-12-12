import {faBalanceScale, faBuilding, faCalculator, faCalendarAlt, faCalendarDay, faClock, faDollar, faDollarSign, faEllipsisH, faFlag, faHospital, faImage, faLanguage, faLocation, faMapMarkerAlt, faPercent, faPerson, faUser, faUsers} from "@fortawesome/free-solid-svg-icons";
import {IconProp} from "@fortawesome/fontawesome-svg-core";
import {faSketch} from "@fortawesome/free-brands-svg-icons";

export const node_style: {[key:string]: {
        color: {[key: string]: string}
        icon: IconProp,
    }} = {
    'PERSON': {
        color: {
            'highlight': '#76bbff',
            'secondary-highlight': '#3280cc',
            'idle': '#0d579d',
        },
        icon: faUser,
    },
    'ORG': {
        color: {
            'highlight': '#ff8b76',
            'secondary-highlight': '#cc5232',
            'idle': '#9d2b0d',
        },
        icon: faBuilding,
    },
    'GPE': {
        color: {
            'highlight': '#76ff8b',
            'secondary-highlight': '#32cc52',
            'idle': '#0d9d2b',
        },
        icon: faFlag,
    },
    'LOC': {
        color: {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
        icon: faMapMarkerAlt,
    },
    'PRODUCT': {
        color: {
            'highlight': '#ffbb76',
            'secondary-highlight': '#cc8032',
            'idle': '#9d570d',
        },
        icon: faSketch,
    },
    'EVENT': {
        color: {
            'highlight': '#bb76ff',
            'secondary-highlight': '#8032cc',
            'idle': '#570d9d',
        },
        icon: faCalendarDay,
    },
    'WORK_OF_ART': {
        color: {
            'highlight': '#bbff76',
            'secondary-highlight': '#80cc32',
            'idle': '#579d0d',
        },
        icon: faImage,
    },
    'LAW': {
        color: {
            'highlight': '#76ffbb',
            'secondary-highlight': '#32cc80',
            'idle': '#0d9d57',
        },
        icon: faBalanceScale,
    },
    'LANGUAGE': {
        color: {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
        icon: faLanguage,
    },
    'DATE': {
        color: {
            'highlight': '#76bbff',
            'secondary-highlight': '#3280cc',
            'idle': '#0d579d',
        },
        icon: faCalendarAlt,
    },
    'TIME': {
        color: {
            'highlight': '#ff8b76',
            'secondary-highlight': '#cc5232',
            'idle': '#9d2b0d',
        },
        icon: faClock,
    },
    'PERCENT': {
        color: {
            'highlight': '#76ff8b',
            'secondary-highlight': '#32cc52',
            'idle': '#0d9d2b',
        },
        icon: faPercent,
    },
    'MONEY': {
        color: {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
        icon: faDollarSign,
    },
    'QUANTITY': {
        color: {
            'highlight': '#ffbb76',
            'secondary-highlight': '#cc8032',
            'idle': '#9d570d',
        },
        icon: faEllipsisH,
    },
    'ORDINAL': {
        color: {
            'highlight': '#bb76ff',
            'secondary-highlight': '#8032cc',
            'idle': '#570d9d',
        },
        icon: faCalculator,
    },
    'CARDINAL': {
        color: {
            'highlight': '#bbff76',
            'secondary-highlight': '#80cc32',
            'idle': '#579d0d',
        },
        icon: faCalculator,
    },
    'FAC': {
        color: {
            'highlight': '#76ffbb',
            'secondary-highlight': '#32cc80',
            'idle': '#0d9d57',
        },
        icon: faHospital,
    },
    'NORP': {
        color: {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
        icon: faUsers,
    },
};