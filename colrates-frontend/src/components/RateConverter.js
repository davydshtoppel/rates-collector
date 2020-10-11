import React from "react";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import CurrenciesDropdown from "./Currencies";


class RateConverter extends React.Component {

  render() {
    return (
        <Container>
            <Row>
                <Col>
                    <InputGroup className="mb-3">
                        <InputGroup.Prepend>
                            <InputGroup.Text id="inputGroup-sizing-default">Count</InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl aria-label="Default" aria-describedby="inputGroup-sizing-default"/>
                    </InputGroup>
                </Col>
                <Col>
                    <CurrenciesDropdown/>
                </Col>
            </Row>
            <Row>
                <Col>
                    <InputGroup className="mb-3">
                        <InputGroup.Prepend>
                            <InputGroup.Text id="inputGroup-sizing-default">Count</InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl aria-label="Count" aria-describedby="inputGroup-sizing-default"/>
                    </InputGroup>
                </Col>
                <Col>
                    <CurrenciesDropdown/>
                </Col>
            </Row>
        </Container>
    );
  }
}

export default RateConverter;

