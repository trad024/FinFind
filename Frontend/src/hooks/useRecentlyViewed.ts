"use client";

import { useState, useEffect, useCallback } from "react";
import type { ProductSearchResult } from "@/types";

const STORAGE_KEY = "finfind_recently_viewed";
const MAX_ITEMS = 10;

export interface RecentlyViewedItem {
  id: string;
  name: string;
  price: number;
  imageUrl?: string;
  category: string;
  brand?: string;
  viewedAt: number;
}

/**
 * Hook to manage recently viewed products
 */
export function useRecentlyViewed() {
  // Initialize state from localStorage
  const [items, setItems] = useState<RecentlyViewedItem[]>(() => {
    if (typeof window === "undefined") return [];
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as RecentlyViewedItem[];
        const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
        return parsed.filter((item) => item.viewedAt > thirtyDaysAgo);
      }
    } catch (error) {
      console.error("Failed to load recently viewed:", error);
    }
    return [];
  });
  const [isLoaded, setIsLoaded] = useState(false);

  // Mark as loaded on mount
  useEffect(() => {
    setIsLoaded(true);
  }, []);

  // Save to localStorage when items change
  useEffect(() => {
    if (isLoaded && typeof window !== "undefined") {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    }
  }, [items, isLoaded]);

  /**
   * Add a product to recently viewed
   */
  const addItem = useCallback((product: ProductSearchResult | RecentlyViewedItem) => {
    setItems((prev) => {
      // Remove if already exists
      const filtered = prev.filter((item) => item.id !== product.id);
      
      // Create new item
      const newItem: RecentlyViewedItem = {
        id: product.id,
        name: product.name,
        price: product.price,
        imageUrl: "imageUrl" in product ? product.imageUrl : undefined,
        category: product.category,
        brand: product.brand,
        viewedAt: Date.now(),
      };
      
      // Add to beginning and limit to MAX_ITEMS
      return [newItem, ...filtered].slice(0, MAX_ITEMS);
    });
  }, []);

  /**
   * Remove a product from recently viewed
   */
  const removeItem = useCallback((productId: string) => {
    setItems((prev) => prev.filter((item) => item.id !== productId));
  }, []);

  /**
   * Clear all recently viewed items
   */
  const clearAll = useCallback(() => {
    setItems([]);
    if (typeof window !== "undefined") {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  return {
    items,
    addItem,
    removeItem,
    clearAll,
    isLoaded,
  };
}
