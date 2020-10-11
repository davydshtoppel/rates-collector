import React from "react";
import ReactDOM from "react-dom";
import AlertRate from "./Rates";
import CurrenciesDropdown from "./Currencies";
import RateConverter from "./RateConverter";
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends React.Component {
  // constructor(props) {
  //   super(props);
  //   this.state = {
  //     data: [],
  //     loaded: false,
  //     placeholder: "Loading"
  //   };
  // }

  // componentDidMount() {
  //   fetch("api/latest?base=EUR")
  //     .then(response => {
  //       if (response.status > 400) {
  //         return this.setState(() => {
  //           return { placeholder: "Something went wrong!" };
  //         });
  //       }
  //       return response.json();
  //     })
  //     .then(data => {
  //       this.setState(() => {
  //         return {
  //           data,
  //           loaded: true
  //         };
  //       });
  //     });
  // }

  render() {
    return (
      // <AlertRate base="EUR" currency="RUB" />
      <RateConverter/>
    );
  }
}

export default App;

const container = document.getElementById("app");
ReactDOM.render(<App />, container);