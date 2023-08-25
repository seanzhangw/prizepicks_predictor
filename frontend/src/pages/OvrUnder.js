import IndiButton from "../components/SportSelect";
import Container from "react-bootstrap/esm/Container";
import ModeSelect from "../components/ListGroup"
import { IMAGES } from '../components/constants.js';
import Row from 'react-bootstrap/Row';
import { useState } from "react";

/* TODO: add conditional rendering to when a sport is selected and keep the selected sport highlighted*/
export default function OvrUnder() {
    const [selectedSport, setSelectedSport] = useState("NBA")
    const [selectedMode, setSelectedMode] = useState("pp")

    return (
        <Container className = "page-wrapper">
            <Row className = 'nav-container'>
            {IMAGES.map((image, index) => (
                <IndiButton key={index} src={image.src} srcalt={image.srcalt} alt={image.alt} label={image.label} />
            ))}
            </Row>
            <Row className = 'header'>
                <ModeSelect/>
            </Row>
        </Container>
    );
}

