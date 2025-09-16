"use client";

import { useContext } from "react";
import { Card, Button, Row, Col, Container } from "react-bootstrap";
import CoursesContext from "@/contexts/DataContext";
import Link from "next/link";

function Dashboard() {
  const { data: courses, isLoading } = useContext(CoursesContext);

  if (isLoading) {
    return <div>Loading...</div>; // Show loading state while fetching data
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
                    <span className="text-white">View Course</span>{" "}
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
