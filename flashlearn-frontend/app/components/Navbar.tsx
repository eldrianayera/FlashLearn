import Link from "next/link";
import React from "react";

export default function Navbar() {
  return (
    <nav className="flex justify-between mx-auto px-15 py-5 border-1 ">
      <Link href="/">FlashLearn</Link>
      <div className="flex gap-12">
        <Link href="dashboard">Dashboard</Link>
        <Link href="login">Login</Link>
        <Link href="signup">SignUp</Link>
      </div>
    </nav>
  );
}
