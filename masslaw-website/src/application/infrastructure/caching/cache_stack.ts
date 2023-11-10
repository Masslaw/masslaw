import assert from "assert";

export class CacheStack<T> {

    private stack: { [key: string]: CacheEntry<T>|undefined };

    private maximum_stack_size?: number;
    private data_loading_function: (key: string) => Promise<T|null>;
    private entry_size_measuring_function?: (e: T) => number;
    private local_cache_key?: string;

    constructor(
        data_loading_function: (key: string) => Promise<T|null>,
        maximum_size?: number,
        entry_size_measuring_function?: (e: T) => number,
        local_cache_key?: string,
    ) {
        this.stack = {}
        this.maximum_stack_size = maximum_size;
        this.data_loading_function = data_loading_function;
        this.entry_size_measuring_function = entry_size_measuring_function;
        this.local_cache_key = local_cache_key;
    }

    public set_maximum_size(size: number) {
        this.maximum_stack_size = size;
        this.handleStackSize();
    }

    public getCached(key: string) : T|null {
        let cached: CacheEntry<T>|undefined = this.stack[key];
        if (cached && !cached.loading) {
            cached.access_count += 1;
            return cached.data
        }
        return null;
    }

    public async loadEntryIfNotLoading(key: string) {
        let cached: CacheEntry<T>|undefined = this.stack[key];
        if (cached?.loading) return;
        this.setEntryLoading(key, true);
        let data = await this.data_loading_function(key);
        if (data) this.cacheData(key, data);
        this.setEntryLoading(key, false);
    }

    public cacheData(key: string, data: T) {
        let entry = this.stack[key] || { data: {} as T, access_count: 0, loading: false } as CacheEntry<T>;
        entry.data = data;
        this.updateEntry(key, entry);
    }

    private setEntryLoading(key: string, loading: boolean) {
        let entry = this.stack[key] || { data: {} as T, access_count: 0, loading: false } as CacheEntry<T>;
        entry.loading = loading;
        this.updateEntry(key, entry);
    }

    private updateEntry(key: string, entry: CacheEntry<T>) {
        this.stack[key] = entry;
        this.handleStackSize();
    }

    private handleStackSize(){
        while (true) {
            const current_stack_size = this.calculateStackSize()
            if (!this.maximum_stack_size || current_stack_size < this.maximum_stack_size) break;
            this.removeLeastAccessCacheEntry();
        }
    }

    private calculateStackSize() {
        let stack_size = 0;
        for (let [key, entry] of Object.entries(this.stack)) {
            if (!entry) continue;
            stack_size += this.getEntryDataSize(entry.data);
        }
        return stack_size
    }

    private getEntryDataSize(entry_data: T): number {
        return this.entry_size_measuring_function &&
            this.entry_size_measuring_function(entry_data) ||
            JSON.stringify(entry_data).length
    }

    private removeLeastAccessCacheEntry() {
        let least_accessed_key = undefined;
        let least_accessed_access_count = Number.MAX_VALUE;
        for (let [key, entry] of Object.entries(this.stack)) {
            if (!entry) continue;
            if (entry.access_count < least_accessed_access_count) {
                least_accessed_key = key;
                least_accessed_access_count = entry.access_count
            }
        }
        if (least_accessed_key) {
            this.removeCachedEntry(least_accessed_key);
        }
    }

    public removeCachedEntry(key: string) {
        delete this.stack[key];
    }

    public saveToLocalStorage() {
        assert(this.local_cache_key);
        localStorage.setItem(this.local_cache_key, JSON.stringify(this.stack));
    }

    public loadFromLocalCache() {
        assert(this.local_cache_key);
        const saved = localStorage.getItem(this.local_cache_key);
        if (saved) this.stack = JSON.parse(saved);
    }

    public saveToSessionStorage() {
        assert(this.local_cache_key);
        sessionStorage.setItem(this.local_cache_key, JSON.stringify(this.stack));
    }

    public loadFromSessionCache() {
        assert(this.local_cache_key);
        const saved = sessionStorage.getItem(this.local_cache_key);
        if (saved) this.stack = JSON.parse(saved);
    }
}

interface CacheEntry<T> {
    data: T,
    access_count: number,
    loading: boolean,
}
