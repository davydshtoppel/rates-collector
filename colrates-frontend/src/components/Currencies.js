import React from "react";
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';

class CurrenciesDropdown extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            loaded: false,
            data: [],
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch(`api/currencies`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        data: result.currencies
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            );
    }

  render() {
    return (
        <DropdownButton id="dropdown-basic-button" title="Currency">
            {this.state.data.map(currency => {
                return (<Dropdown.Item href="#">{currency}</Dropdown.Item>);
            })}
        </DropdownButton>
    );
  }
}

export default CurrenciesDropdown;

