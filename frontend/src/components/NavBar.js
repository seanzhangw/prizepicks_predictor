import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useState } from 'react';
import { useLocation } from 'react-router-dom';

function NavBar() {
  const [hoveredLink,setHoveredLink] = useState('')
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  const handleMouseEntry = (link) => {
    setHoveredLink(link)
  }

  const handleMouseExit = () => {
    setHoveredLink('')
  }

  const getStyle = (link) => ({
    color: hoveredLink === link ? 'white' : 'gray'
  })

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
            <Nav.Link 
              onMouseEnter={() => handleMouseEntry('/over_under')}
              onMouseLeave={handleMouseExit} 
              style = {getStyle('/over_under')} 
              href="over_under"
              className={isActive('/over_under') ? 'active-link' : ''}
            >
              Over/Under
            </Nav.Link>
            <Nav.Link 
              onMouseEnter={() => handleMouseEntry('/w_l')} 
              onMouseLeave={handleMouseExit}
              style = {getStyle('/w_l')} 
              href="w_l"
              className={isActive('/w_l') ? 'active-link' : ''}
            >
              Win-Loss
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;