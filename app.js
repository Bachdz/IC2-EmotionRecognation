const express = require("express");
const bodyParser = require('body-parser');
require('dotenv').config();

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

// Make static uses
app.use(express.static(__dirname + '/public'));


// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({extended: true}));

// parse application/json
app.use(bodyParser.json());

app.listen(port, () => console.log(`Server started listening on port: ${port}`));