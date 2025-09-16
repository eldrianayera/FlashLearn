"use client";

import axios from "axios";
import { FormEvent, useState } from "react";

interface LogInData {
  username: string;
  password: string;
}

export default function SignUp() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string>("");

  const handleSignUp = (e: FormEvent) => {
    e.preventDefault();

    async function postData() {
      const data: LogInData = {
        username,
        password,
      };

      try {
        const response = await axios.post(
          "http://localhost:8000/api/auth/login/",
          data,
          {
            headers: {
              "Content-Type": "application/json", // Indicate the body format
            },
          }
        );

        const access_token = response.data.access;
        console.log(access_token);

        localStorage.setItem("access_token", access_token);
      } catch (error) {
        if (axios.isAxiosError(error)) {
          if (error.response) {
            console.error("Error Response:", error.response.data);
            console.error("Error Status:", error.response.status);
            console.error("Error Headers:", error.response.headers);
            console.error("Error Message:", error.response.headers);
          } else if (error.request) {
            // If the request was made but no response was received
            console.error("Error Request:", error.request);
          } else {
            // Something else triggered the error
            console.error("Error Message:", error.message);
          }
        } else {
          console.error("Unexpected Error:", error);
        }
      }
    }

    postData();
  };

  return (
    <section className="login-page flex justify-center items-center min-h-screen bg-gray-100 p-4">
      <form
        onSubmit={handleSignUp}
        className="flex flex-col bg-white p-8 rounded-lg shadow-lg w-full max-w-md"
      >
        <h2 className="text-2xl font-bold text-center mb-6">Log In</h2>

        <div className="flex flex-col mb-4">
          <label
            htmlFor="username"
            className="text-sm font-medium text-gray-700"
          >
            Username
          </label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="Enter username"
            onChange={(e) => setUsername(e.target.value)}
            className="mt-2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="flex flex-col mb-4">
          <label
            htmlFor="password"
            className="text-sm font-medium text-gray-700"
          >
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Enter password"
            onChange={(e) => setPassword(e.target.value)}
            className="mt-2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Log In
        </button>
      </form>
    </section>
  );
}
