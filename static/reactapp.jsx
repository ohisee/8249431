{ /* some comments*/ }
class App extends React.Component {
	constructor() {
		super();
		this.state = {
			data: [
        {
					"id": 1,
					"name": "line 1",
					"location": "unknown"
				},
				{
					"id": 2,
					"name": "line 2",
					"location": "unknown"
				},
				{
					"id": 3,
					"name": "line 3",
					"location": "unknown"
				}
			]
		};
	}
	render() {
		return(
			<div>
        <Header/>
        <Content/>
        <table>
          <tbody>
            {this.state.data.map((value)=><TableRow data={value}/>)}
          </tbody>
        </table>
      </div>
		);
	}
}

class Header extends React.Component {
	render() {
		var hstyle = {
			fontSize: 20,
			color: '#FF0000'
		};
		return(
			<div>
        <h2 style={hstyle}>
          Content Header
        </h2>
      </div>
		);
	}
}

class Content extends React.Component {
	render() {
		return(
			<p>
        Hello World, another example, more examples
      </p>
		);
	}
}

class TableRow extends React.Component {
	render() {
		return(
			<tr>
        <td>{this.props.data.name}</td>
      </tr>
		);
	}
}

{ /* Start to render */ }
ReactDOM.render(
	<App />,
	document.getElementById('app')
);
