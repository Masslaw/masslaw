export function mergeDeep(merge_to, merge_from) {
    if (typeof merge_to !== typeof merge_from) return merge_from;
    if (typeof merge_to !== 'object') return merge_from;
    if (Array.isArray(merge_to)) return [...merge_to, ...merge_from];
    merge_to = {...merge_to};
    for (const key in merge_from) merge_to[key] = mergeDeep(merge_to[key], merge_from[key]);
    return merge_to;
}
