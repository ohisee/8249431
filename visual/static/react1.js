/*
 * Use react js to build CommentBox.
 */
var CommentBox = React.createClass({
  render: function() {
    return (
      <div className="commentBox">Hello World!!!</div>
    );
  }
});

React.render(
  <CommentBox />, document.getElementById('content')
);
