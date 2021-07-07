/** @jsx React.DOM */
var GRID_SIZE = 40;

var BoardIntersection = React.createClass({
    handleClick: function() {
        if (this.props.board.play(this.props.row, this.props.col))
            this.props.onPlay();
    },
    render: function() {
        var style = {
            top: this.props.row * GRID_SIZE,
            left: this.props.col * GRID_SIZE
        };
    }
})