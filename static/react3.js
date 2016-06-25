/*
 *
 */
var data = [
  {author: "Pete Hunt", text: "This is one one one comment"},
  {author: "Jordan Walke", text: "This is *another* one one one comment"}
];

/*
 * Comment object.
 */
var Comment = React.createClass({
   render: function() {
     return (
       <div className="comment">
         <h2 className="commentAuthor">
           {this.props.author}
         </h2>
         {this.props.children}
       </div>
     );
   }
 });

var CommentList = React.createClass({
  render: function() {
    var commentNodes = this.props.data.map(function (comment) {
      return (
        <Comment author={comment.author}>
          {comment.text}
        </Comment>
      );
    });
    return (
      <div className="commentList">{commentNodes}</div>
    );
  }
});

var CommentForm = React.createClass({
  render: function() {
    return (
      <div className = "commentForm">Hello World!&nbsp;This is a comment form.</div>
    );
  }
});

var CommentBox = React.createClass({
  render: function() {
    return (
      <div className="commentBox">
        <h1>Comments</h1>
        <CommentList data={this.props.data}/>
        <CommentForm />
      </div>
    );
  }
});

React.render(
  <CommentBox data={data}/>, document.getElementById("content")
);
