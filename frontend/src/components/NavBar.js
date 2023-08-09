import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function NavBar() {
  return (
    <Navbar expand="lg" className="bg-dark">
      <Container fluid>
        <Navbar.Brand href="home">
            <img 
                src = "/pp.png"
                alt = "PP logo"
                width = "45"
                height = "45"
                className = "d-inline-block align-top"
                style= {{ marginLeft: 15}}
            />
        <span style={{ color:"white", fontSize: '25px', fontWeight: 'bold', marginLeft: 15, lineHeight: '50px'}}>PRIZESPICKED</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link style = {{color: "white"}} href="over_under">Over/Under</Nav.Link>
            <Nav.Link style = {{color: "white"}} href="w_l">Win-Loss</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;