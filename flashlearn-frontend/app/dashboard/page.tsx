"use client";

import { useContext, useEffect, useState } from "react";
import { Card, Button, Row, Col, Container } from "react-bootstrap";
import CoursesContext from "@/contexts/DataContext";
import Link from "next/link";
import AuthContext from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";

function Dashboard() {
  const { data: courses, isLoading: courseLoading } =
    useContext(CoursesContext);
  const { isAuthenticated, isLoading: authLoading } = useContext(AuthContext);
  const router = useRouter();
  const [isAuthenticatedChecked, setIsAuthenticatedChecked] = useState(false);

  useEffect(() => {
    if (authLoading) return; // Wait for authentication loading state to finish
    if (!isAuthenticated) {
      router.push("/login"); // Redirect to login if not authenticated
    }
    setIsAuthenticatedChecked(true); // Mark authentication as checked
  }, [isAuthenticated, authLoading]);

  // Loading state for both authentication and courses
  if (authLoading || !isAuthenticatedChecked) {
    return (
      <div className="text-center">
        <p>Authenticating...</p> {/* Show authentication loading */}
      </div>
    );
  }

  if (courseLoading) {
    return (
      <div className="text-center">
        <p>Loading courses...</p> {/* Show loading while fetching courses */}
      </div>
    );
  }

  return (
    <Container className="mt-4">
      <h1 className="text-center mb-4">Dashboard</h1>
      <Row className="g-4">
        {courses.map((course) => (
          <Col md={4} key={course.id}>
            <Card className="shadow-sm border-light rounded">
              <Card.Body>
                <Card.Title className="text-center mb-3">
                  {course.name}
                </Card.Title>

                <Button variant="primary" className="w-100">
                  <Link href={`/dashboard/${course.id}`} passHref>
                    <span className="text-white">View Course</span>
                  </Link>
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default Dashboard;
