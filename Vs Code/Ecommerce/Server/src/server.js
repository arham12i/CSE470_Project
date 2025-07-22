const express = require("express");
const morgan = require("morgan");
const app = express();

app.use(morgan('dev'));


app.get('/test', (req, res) => {
    res.status(200).send({
        message: 'Welcome to get the server',
    });
});

app.post('/test', (req, res) => {
    res.status(200).send({
        message: 'Welcome to the post server',
    });
});

app.put('/test', (req, res) => {
    res.status(200).send({
        message: 'Welcome to put the server',
    });
});

app.delete('/test', (req, res) => {
    res.status(200).send({
        message: 'Welcome to delete the server',
    });
});

app.listen(3001, ()=> {
    console.log('Server is running at http://localhost:3001');
});