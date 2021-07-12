//globals
var rootX = 60, rootY = 45
var boardSize = 9 // TODO make this a user choice between 9, 13 or 18  
var boxSize = 50;

window.onload = function() {
    var canvas = document.getElementsByTagName('canvas')[0];
    var ctx = canvas.getContext('2d');  

    // i think these only render what is visible?
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    drawBoard(ctx); 
}

// function to draw the go board
function drawBoard(ctx) {

    var x = rootX, y = rootY

    ctx.lineWidth = 2;
    ctx.beginPath();

    ctx.fillStyle = '#eaf1f3'

    ctx.fillRect(rootX - 40, rootY - 40, 80 + boxSize * (boardSize - 1), 80 + boxSize * (boardSize - 1));

    for(var i = 0; i < boardSize; i++){ // for i in range loop, i++ auto-increments
        drawLine(ctx, x, y, 0, boxSize * (boardSize - 1));
        x += boxSize;
    }
    x = rootX, y = rootY;
    for(var i = 0; i < boardSize; i++){ // for i in range loop, i++ auto-increments
        drawLine(ctx, x, y, boxSize * (boardSize- 1), 0);
        y += boxSize;
    }

    drawLine(ctx, rootX - 40, rootY - 40, 0, 80 + boxSize * (boardSize - 1));
    drawLine(ctx, rootX + 40 + boxSize * (boardSize - 1), rootY - 40, 0, 80 + boxSize * (boardSize - 1));
	drawLine(ctx, rootX - 40, rootY - 40, 80 + boxSize * (boardSize - 1), 0);
	drawLine(ctx, rootX - 40, rootY + 40 + boxSize * (boardSize - 1), 80 + boxSize * (boardSize - 1), 0);

    ctx.fillStyle = '#495755';
	drawPoint(ctx, 2, 2);
	drawPoint(ctx, 2, 6);   
	drawPoint(ctx, 6, 2);
	drawPoint(ctx, 6, 6);
	drawPoint(ctx, 4, 4);	

}   
// function to draw lines for the board (shocking)
function drawLine(ctx, x, y, a, b) {
    ctx.moveTo(x, y);
    ctx.lineTo(x + a, y + b);   
    ctx.Stroke();
}

function drawPoint(ctx, x, y){
    ctx.beginPath();
    ctx.arc(rootX + boxSize * x, rootY + boxSize * y, 5, 0, 2 * Math.PI);
    ctx.fill();
}