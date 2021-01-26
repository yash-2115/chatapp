import React from 'react';
import axios from 'axios';

class App extends React.Component {

	state = {
    details: [],
    user: "",

  };

    handleInput = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

	componentDidMount() {

		let data ;

		axios.get('http://127.0.0.1:8000/')
		.then(res => {
			data = res.data;
			this.setState({
				details : data
			});
		})
		.catch(err => {})
	}

render() {
	return(
	<div>
			{this.state.details.map((detail, id) => (
			<div key={id}>
			<div >
				<div >
						<h1>{detail.name} </h1>

				</div>
			</div>
			</div>
			)
		)}
	</div>
	);
}
}

export default App;