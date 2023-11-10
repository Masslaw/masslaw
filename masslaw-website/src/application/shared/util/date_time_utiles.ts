export function unixTimeToDateTimeString(unixTime: number): string {
    if (unixTime < 10) return 'Unknown'
    const date = new Date(unixTime * 1000); // convert from seconds to milliseconds
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear().toString();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

export function unixTimeToPastTimeString(unixTime: number): string {
    const now = Date.now();
    const diffInSeconds = Math.floor((now - unixTime * 1000) / 1000);

    if (diffInSeconds < 60) {
        return `${diffInSeconds} seconds ago`;
    }
    else if (diffInSeconds < 3600) {
        return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    }
    else if (diffInSeconds < 86400) {
        return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    }
    else {
        return `${Math.floor(diffInSeconds / 86400)} days ago`;
    }
}

export function asyncSleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function formatOrdinal(n: number): string {
    const s = ["th", "st", "nd", "rd"];
    const v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

export function unixTimeToDayDateString(unixEpoch: number): string {
    const date = new Date(unixEpoch * 1000); // Convert to milliseconds
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];

    const day = formatOrdinal(date.getDate());
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();

    return `${month} ${day} ${year}`;
}