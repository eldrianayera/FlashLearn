"use client";

import axios from "axios";
import React, { useEffect, useState } from "react";

function Dashboard() {
  const [couses, setCouses] = useState();

  useEffect(() => {
    const fetchData = async () => {
      const access_token = localStorage.getItem("access_token");

      try {
        const response = await axios.get("http://localhost:8000/api/courses/", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${access_token}`,
          },
        });

        console.log(response.data);
      } catch (error) {}
    };

    fetchData();
  }, []);

  return <div>Dashboard</div>;
}

export default Dashboard;
