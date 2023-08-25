import Button from 'react-bootstrap/Button';
import { useState } from 'react';

 
function IndiButton(props) {
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
                src={hovered ? '/sport_icons/' + props.srcalt : '/sport_icons/' + props.src}
                alt={props.alt}
                style={{
                    width: '35px',
                    height: '35px',
                }}
            />
            <span style={{fontSize: 16, fontWeight: 'bold', fontFamily: 'IndustryBook'
            }}>{props.label}</span>
      </Button>
    )
}

export default IndiButton;