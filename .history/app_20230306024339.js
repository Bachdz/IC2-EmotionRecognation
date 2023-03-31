const express = require("express");
const bodyParser = require('body-parser');
require('dotenv').config();
const { errorHandler } = require('./middlewares/errorMiddleware')
const { Server } = require("socket.io");
const { createServer } = require("http");


const app = express();

const port = process.env.PORT || 8000;





//Bodyparser
app.use(express.urlencoded({
    extended: false
}));

app.set('view engine', 'ejs');



// Routes
app.use('/', require('./routes/index'));
app.use('/detect', require('./routes/detector'));
app.use(errorHandler)

// Make static uses
app.use(express.static(__dirname + '/public'));


// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({extended: true}));

// parse application/json
app.use(bodyParser.json());

const httpServer = createServer(app);

const io = new Server(httpServer, { /* options */ });


io.on("connection", (socket) => {
    console.log("New client connected");

    socket.on('face', (data) => {
        console.log("got face data");
        socket.broadcast.emit('face', data);
    })

    socket.on('emotion-detected', (data) => {
        console.log("got emotion data");
        socket.broadcast.emit('emotion', data);
    })

    socket.on('no-face', (data) => {
        console.log("no face detected");
        socket.broadcast.emit('no-face', data);
    })

    socket.on('error', (data) => {
        console.log("error", data);
        socket.broadcast.emit('error', data);
    })



    socket.on("disconnect", () => {
        console.log("Client disconnected");
    });

});




httpServer.listen(port, () => console.log(`Server started listening on port: ${port}`));