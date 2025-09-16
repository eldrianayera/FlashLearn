"use client";

import axios from "axios";
import { FormEvent, useState } from "react";

interface FormData {
  username: string;
  email: string;
  password1: string;
  password2: string;
}

export default function SignUp() {
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password1, setPassword1] = useState<string>("");
  const [password2, setPassword2] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string>("");

  const handleSignUp = (e: FormEvent) => {
    e.preventDefault();

    async function postData() {
      const data: FormData = {
        username,
        email,
        password1,
        password2,
      };

      try {
        const response = await axios.post(
          "http://localhost:8000/api/auth/registration/",
          data,
          {
            headers: {
              "Content-Type": "application/json", // Indicate the body format
            },
          }
        );

        console.log(response.data);
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

    if (password1 != password2) {
      setErrorMsg("Passwords doesn't match");
    } else {
      postData();
    }
  };

  return (
    <section className="login-page flex justify-center items-center min-h-screen bg-gray-100 p-4">
      <form
        onSubmit={handleSignUp}
        className="flex flex-col bg-white p-8 rounded-lg shadow-lg w-full max-w-md"
      >
        <h2 className="text-2xl font-bold text-center mb-6">Sign Up</h2>

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
          <label htmlFor="email" className="text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="Enter email"
            onChange={(e) => setEmail(e.target.value)}
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
            onChange={(e) => setPassword1(e.target.value)}
            className="mt-2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="flex flex-col mb-6">
          <label
            htmlFor="password2"
            className="text-sm font-medium text-gray-700"
          >
            Confirm Password
          </label>
          <input
            type="password"
            id="password2"
            name="password2"
            placeholder="Confirm your password"
            onChange={(e) => setPassword2(e.target.value)}
            className="mt-2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <p>{errorMsg}</p>

        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Sign Up
        </button>
      </form>
    </section>
  );
}
