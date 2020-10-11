import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';

class AlertRate extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch(`api/latest?base=${this.props.base}&currency=${this.props.currency}`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        date: result.date,
                        rate: result.rates[0].values[0].rate
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
        <div class="alert alert-success" role="alert">
            {this.state.date} from {this.state.rate}
        </div>
    );
  }
}

export default AlertRate;
