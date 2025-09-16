"use client";

import CoursesContext from "@/contexts/DataContext";
import React, { useContext, useEffect, useState } from "react";

function Dashboard() {
  const { data: courses, isLoading } = useContext(CoursesContext);

  return (
    <div>
      Dashboard
      <div>
        {courses.map((course) => {
          return <div key={course.id}>{course.name}</div>;
        })}
      </div>
    </div>
  );
}

export default Dashboard;
