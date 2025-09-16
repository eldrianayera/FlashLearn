"use client";

import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { createContext, ReactNode, useState, useEffect } from "react";

// Define Types
export interface FlashcardType {
  id: number;
  answer: string;
  question: string;
  document: number;
}

export interface DocumentType {
  course: number;
  id: number;
  created_at: Date;
  updated_at: Date;
  file: string;
  flashcards?: FlashcardType[];
  name: string;
  summary?: string;
}

export interface CourseType {
  course_note?: string;
  created_at: Date;
  updated_at: Date;
  documents?: DocumentType[];
  name: string;
  id: number;
  user: number;
}

export interface CoursesContext {
  data: CourseType[];
  isLoading: boolean;
}

// Default context value
const defaultData: CoursesContext = {
  data: [],
  isLoading: true,
};

// Create Context
const CoursesContext = createContext<CoursesContext>(defaultData);

// CoursesContextProvider component
export const CoursesContextProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);

  // UseEffect to only get the access token on the client-side
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setAccessToken(token); // Store token in state
  }, []);

  // Fetch courses using `useQuery` when the token is available
  const { data: courses, isLoading } = useQuery({
    queryKey: ["allCourses"],
    queryFn: async () => {
      if (!accessToken) {
        throw new Error("No access token found");
      }

      const { data } = await axios.get("http://localhost:8000/api/courses/", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });

      return data; // Assuming the response returns the courses data directly
    },
    enabled: !!accessToken, // Only run the query if we have an access token
  });

  return (
    <CoursesContext.Provider value={{ data: courses || [], isLoading }}>
      {children}
    </CoursesContext.Provider>
  );
};

export default CoursesContext;
