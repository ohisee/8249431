{/* some comments*/}
class App extends React.Component {
  render() {
    return (
      <div>
        <Header/>
        <Content/>
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
    return (
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
    return (
      <p>
        Hello World, another example, more examples
      </p>
    )
  }
}

{/* Start to render */}
ReactDOM.render(
  <App />,
  document.getElementById('app')
);
