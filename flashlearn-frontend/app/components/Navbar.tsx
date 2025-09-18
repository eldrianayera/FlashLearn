"use client";

import AuthContext from "@/contexts/AuthContext";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useContext, useEffect } from "react";

export default function Navbar() {
  const { isAuthenticated, isLoading, logIn, logOut } = useContext(AuthContext);

  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push("/dashboard");
    }
    console.log(isAuthenticated);
  }, [isAuthenticated]);

  const handleLogOut = () => {
    logOut();
    router.push("/login");
  };

  return (
    <nav className="flex justify-between mx-auto px-15 py-5 border-1 ">
      <Link href="/">FlashLearn</Link>
      <div className="flex gap-12">
        <Link href="/dashboard">Dashboard</Link>
        {isAuthenticated ? (
          <>
            <button onClick={handleLogOut}>Logout</button>
          </>
        ) : (
          <>
            <Link href="/login">Login</Link>
            <Link href="/signup">SignUp</Link>
          </>
        )}
      </div>
    </nav>
  );
}
