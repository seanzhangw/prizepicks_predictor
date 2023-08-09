import Button from 'react-bootstrap/Button';
import { useState } from 'react';

 
function IndiButton() {
    const [hovered,setHovered] = useState(false);

    const handleMouseEntry = () => {
        setHovered(true);
    }
    
    const handleMouseExit = () => {
        setHovered(false);
    }

    const textStyle = {
        backgroundColor: hovered ? 'white' : 'black',
        color: hovered ? 'black' : 'gray',
        padding: '10px',
        margin: '10px',
        borderRadius: '25px',
        borderColor: 'black',
        transition: 'color .3s',
        width: '80px',
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center' 
    };

    return (
        <Button
            variant='dark' 
            style={textStyle}
            onMouseEnter={(handleMouseEntry)}
            onMouseLeave={(handleMouseExit)}
        >
            <img
                src={hovered ? '/bsktballw.png': '/bsktball.png'}
                alt="fix" 
                style={{
                    width: '35px',
                    height: '35px',
                }}
            />
            <span style={{fontSize: 16, fontWeight: 'bold', fontFamily: 'IndustryBook'
            }}>NBA</span>
      </Button>
    )
}

export default IndiButton;