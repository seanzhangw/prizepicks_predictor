import ListGroup from 'react-bootstrap/ListGroup';
import { useState } from 'react';

function ModeSelect() {
  const [activeTab, setActiveTab] = useState("pp")

  const handleClick = (item) => {
    setActiveTab(item)
  }

  const listStyling = {
    pp: activeTab === "pp" ? "custom-list-group-item-active" : "custom-list-group-item-inactive",
    manual: activeTab === "manual" ? "custom-list-group-item-active" : "custom-list-group-item-inactive"
  }

  return (
    <ListGroup className = "custom-list-group" horizontal>
      <ListGroup.Item onClick = {() => handleClick("pp")} className={listStyling.pp}>PrizePicks Lines</ListGroup.Item>
      <ListGroup.Item onClick = {() => handleClick("manual")} className={listStyling.manual}>Manual Entry</ListGroup.Item>
      <ListGroup.Item className = "custom-list-group-item-alt">Help</ListGroup.Item>
    </ListGroup>
  );
}

export default ModeSelect;