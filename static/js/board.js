var Board = function(size) {
    this.current_color = board.BLACK;
    this.size = size;
    this.board = this.create_board();
    this.last_move_passed = false;
    this.in_atari = false;
    this.attempted_suicide = false;
};

board.EMPTY = 0;
board.BLACK = 1;
board.WHITE = 2;

board.prototype.create_board = function(){
    var m = [];
    for (var i = 0; i < 18; i++) {
        m[i] = []
        for (var j = 0; j < 18; j++)
            m[i][j] = board.EMPTY
    }
    return m;
}

// TODO add a function for switching to the second players turn
// TODO check which player session is currently active for making turn

Board.prototype.pass = function(size) {
    if(this.last_move_passed)
        this.end_game();
    this.last_move_passed = true;

}

board.prototype.end_game = function() {
    // delete the data and add a win to the player that won
};

Board.prototype.play = function(i, j){
    console.log("Played at " + i + ", " + j); // debug
    this.attempted_suicide = this.in_atari = false;

    if (this.board[i,j] != board.EMPTY)
        return false;

    var color = this.board[i][j] = this.current_color;
    var captured = []
    var neighbours = this.get_adjacent_intersections(i, j);
    var atari = false;

    var self = this;
    _.each(neighbors, function(n) {
        var state = self.board[n[0]][n[1]];
        if (state != Board.EMPTY && state != color) {
            var group = self.get_group(n[0], n[1]);
            console.log(group);
            if (group["liberties"] == 0)
                captured.push(group);
            else if (group["liberties"] == 1)
                atari = true;
        }
    });

    if (_.isEmpty(captured) && this.get_group(i, j)['liberties'] == 0){
        this.board[i][j] = board.EMPTY;
        this.attempted_suicide = true;
        return false;
    }

    var self = this;
    _.each(captured, function(group) {
        _.each(group['stones'], function(stone) {
            self.board[stone[0]][stone[1]] = board.EMPTY;
        });
    });

    if (atari)
        this.in_atari = true;
    
    this.last_move_passed = false;
    // start next player turn
    return true;
};

Board.prototype.get_adjacent_intersections = function(i, j) { // function for checking adjacent coordinates of a piece
    var color = this.board[i][j];
    if (color == Board.EMPTY)
        return null;
    
    var visited = {};
    var visited_list = [];
    var queue = [[i, j]];
    var count = 0;

    while (queue.length > 0) {
        var stone = queue.pop();
        if (visited[stone])
            continue;

        var neighbors = this.get_adjacent_intersections(stone[0], stone[1]);
        var self = this;
        _.each(neighbors, function(n) {
            var state = self.board[n[0]][n[1]];
            if (state == board.EMPTY) // if the coordinate is not empty
                count++; // ++ increases the value by 1
            if (state == color) // if the coordinate has a piece on it
                queue.push([n[0], n[1]])//
        });

        visited[stone] = true;
        visited_list.push(stone);
    }

    return {
        "liberties": count,
        "stones": visited_list
    };
}