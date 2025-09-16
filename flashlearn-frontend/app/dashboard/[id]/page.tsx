"use client";

import { useContext } from "react";
import {
  Card,
  Button,
  Row,
  Col,
  Container,
  CardBody,
  CardTitle,
  CardText,
} from "react-bootstrap";
import CoursesContext from "@/contexts/DataContext";
import { useParams } from "next/navigation";

function Dashboard() {
  const { id }: { id: string } = useParams();
  const { data: courses, isLoading } = useContext(CoursesContext);

  const selectedCourse = courses.find((c) => c.id == Number(id));

  const handleAddDoc = async () => {};

  if (isLoading) {
    return <div>Loading...</div>; // Show loading state while fetching data
  }

  if (!selectedCourse) {
    return <div>Not found</div>;
  }

  return (
    <Container className="mt-4">
      <h1 className="text-center mb-4">{selectedCourse.name}</h1>
      <button onClick={() => console.log("click")} className="btn btn-primary">
        Add New Document +{" "}
      </button>
      <Row className="g-4">
        <Col md={4} key={selectedCourse.id}>
          {selectedCourse.documents &&
            selectedCourse.documents.map((doc) => (
              <Card key={doc.id}>
                <CardBody>
                  <CardTitle>
                    <h2>{doc.name}</h2>
                  </CardTitle>
                  <CardText>
                    {doc.summary && (
                      <div>
                        <h3>Summary :</h3>
                        <p>{doc.summary}</p>
                      </div>
                    )}
                  </CardText>
                </CardBody>
              </Card>
            ))}
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard;
