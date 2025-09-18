"use client";

import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { createContext, ReactNode, useEffect, useState } from "react";

interface LogInData {
  username: string;
  password: string;
}

interface AuthContext {
  isAuthenticated: boolean;
  isLoading: boolean;
  logIn: ({ username, password }: LogInData) => void;
  logOut: () => void;
}

const defaultData: AuthContext = {
  isAuthenticated: false,
  isLoading: true,
  logIn: () => {},
  logOut: () => {},
};

const AuthContext = createContext<AuthContext>(defaultData);

export const AuthContextProvider = ({ children }: { children: ReactNode }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);

  // UseEffect to only get the access token on the client-side
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setAccessToken(token); // Store token in state
  }, []);

  const {
    data: isAuthenticated,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["auth"],
    queryFn: async () => {
      if (!accessToken) return false;

      try {
        const response = await axios.post(
          "http://localhost:8000/api/auth/token/verify",
          {
            token: accessToken, // Pass token in the request body
          },
          {
            headers: {
              "Content-Type": "application/json", // Set content-type header
            },
          }
        );
        // If response is successful, the token is valid
        console.log("checking", response);

        return response.status === 200;
      } catch (error) {
        console.log("error ", error);
        return false;
      }
    },
    enabled: !!accessToken, // Only run if accessToken exists
  });

  const logIn = async ({ username, password }: LogInData) => {
    const logInData: LogInData = { username, password };
    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/login/",
        logInData,
        {
          headers: {
            "Content-Type": "application/json", // Indicate the body format
          },
        }
      );

      const access_token = response.data.access;

      // Save the access token to localStorage
      localStorage.setItem("access_token", access_token);

      // Optionally, you can manually trigger the `isAuthenticated` state
      setAccessToken(access_token);
      refetch(); // Refetch to update `isAuthenticated`
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  const logOut = async () => {
    try {
      // Send the current access token to the logout API
      await axios.post(
        "http://localhost:8000/api/auth/logout/",
        {
          token: accessToken, // Pass token in the request body
        },
        {
          headers: {
            "Content-Type": "application/json", // Set content-type header
          },
        }
      );

      console.log("Logged out successfully");

      // Remove token from localStorage and clear state
      localStorage.removeItem("access_token");
      setAccessToken(null); // Reset accessToken in state
      refetch(); // Refetch to update `isAuthenticated` to false
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: isAuthenticated || false,
        isLoading,
        logIn,
        logOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
