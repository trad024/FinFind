"use client";

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from "react";

// Demo users matching the backend demo_data.py
export interface DemoUser {
  id: string;
  name: string;
  email: string;
  persona: string;
  avatar?: string;
  profile: {
    occupation: string;
    budgetRange: {
      min: number;
      max: number;
    };
    monthlyBudget: number;
  };
}

export const DEMO_USERS: DemoUser[] = [
  {
    id: "99b53b96-6d17-5a4b-ba92-e995a8a71123",  // demo_student_001
    name: "Sarah Chen",
    email: "sarah.chen@demo.edu",
    persona: "college_student",
    avatar: "SC",
    profile: {
      occupation: "Student",
      budgetRange: { min: 300, max: 800 },
      monthlyBudget: 500,
    },
  },
  {
    id: "666fd4d6-f4bf-592c-b9ab-c3edbeac4a00",  // demo_professional_001
    name: "Marcus Johnson",
    email: "marcus.j@demo.tech",
    persona: "software_engineer",
    avatar: "MJ",
    profile: {
      occupation: "Software Engineer",
      budgetRange: { min: 1000, max: 2500 },
      monthlyBudget: 1500,
    },
  },
  {
    id: "dc2c198d-b816-569f-9d26-3c71020596e7",  // demo_parent_001
    name: "Jennifer Martinez",
    email: "jen.martinez@demo.family",
    persona: "budget_conscious_parent",
    avatar: "JM",
    profile: {
      occupation: "Teacher",
      budgetRange: { min: 200, max: 600 },
      monthlyBudget: 400,
    },
  },
  {
    id: "0f9233b1-7390-515d-9787-175006338642",  // guest
    name: "Guest User",
    email: "guest@finfind.demo",
    persona: "guest",
    avatar: "G",
    profile: {
      occupation: "Guest",
      budgetRange: { min: 0, max: 1000 },
      monthlyBudget: 500,
    },
  },
];

// Default demo user
export const DEFAULT_USER = DEMO_USERS[0];

interface AuthContextType {
  user: DemoUser;
  isAuthenticated: boolean;
  login: (userId: string) => void;
  logout: () => void;
  switchUser: (userId: string) => void;
  availableUsers: DemoUser[];
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const STORAGE_KEY = "finfind_current_user";

// Migration map for old IDs to new UUIDs
const ID_MIGRATION_MAP: Record<string, string> = {
  "demo_student_001": "99b53b96-6d17-5a4b-ba92-e995a8a71123",
  "demo_professional_001": "666fd4d6-f4bf-592c-b9ab-c3edbeac4a00",
  "demo_parent_001": "dc2c198d-b816-569f-9d26-3c71020596e7",
  "demo-user-001": "d486a14c-d0f4-5f8b-aa8f-f50ec0a14de4",
  "guest": "0f9233b1-7390-515d-9787-175006338642",
};

// Migrate old user IDs to new UUIDs
function migrateUserId(oldId: string | null): string | null {
  if (!oldId) return null;
  return ID_MIGRATION_MAP[oldId] || oldId;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<DemoUser>(DEFAULT_USER);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load user from localStorage on mount (with migration)
  useEffect(() => {
    if (typeof window !== "undefined") {
      // Migrate old userId if present
      const legacyUserId = localStorage.getItem("userId");
      const migratedLegacyId = migrateUserId(legacyUserId);
      if (migratedLegacyId && migratedLegacyId !== legacyUserId) {
        localStorage.setItem("userId", migratedLegacyId);
      }

      const storedUserId = localStorage.getItem(STORAGE_KEY);
      const migratedStoredId = migrateUserId(storedUserId);
      
      if (migratedStoredId) {
        const foundUser = DEMO_USERS.find((u) => u.id === migratedStoredId);
        if (foundUser) {
          setUser(foundUser);
        }
      }
      // Also set the legacy userId key for API compatibility
      localStorage.setItem("userId", user.id);
      setIsLoaded(true);
    }
  }, []);

  // Sync userId to localStorage when user changes
  useEffect(() => {
    if (isLoaded && typeof window !== "undefined") {
      localStorage.setItem(STORAGE_KEY, user.id);
      localStorage.setItem("userId", user.id);
    }
  }, [user, isLoaded]);

  const login = useCallback((userId: string) => {
    const foundUser = DEMO_USERS.find((u) => u.id === userId);
    if (foundUser) {
      setUser(foundUser);
    }
  }, []);

  const logout = useCallback(() => {
    const guestUser = DEMO_USERS.find((u) => u.id === "guest") || DEFAULT_USER;
    setUser(guestUser);
  }, []);

  const switchUser = useCallback((userId: string) => {
    login(userId);
  }, [login]);

  const value: AuthContextType = {
    user,
    isAuthenticated: user.id !== "guest",
    login,
    logout,
    switchUser,
    availableUsers: DEMO_USERS,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

// Helper hook for getting just the user ID (for API calls)
export function useUserId(): string {
  const { user } = useAuth();
  return user.id;
}
