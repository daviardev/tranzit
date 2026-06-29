import { LRUCache } from "lru-cache";

const cache = new LRUCache<string, string>({
  max: 500,
  ttl: 1000 * 60 * 60,
});

export function getCached(key: string): string | undefined {
  return cache.get(key);
}

export function setCache(key: string, value: string): void {
  cache.set(key, value);
}

export function hasCache(key: string): boolean {
  return cache.has(key);
}
