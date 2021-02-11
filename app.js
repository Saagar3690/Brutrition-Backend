const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

// Good practice to not use .env files in production and rather set them directly
/*if (process.env.NODE_ENV !== 'production') {
	require('dotenv').config();
}*/

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const uri = /*'mongodb+srv://brutrition:UCLAbru2021@brutrition.qemvx.mongodb.net/Prod?retryWrites=true&w=majority' ||*/ process.env.MONGOLAB_URI;

mongoose.connect(uri, {
	useNewUrlParser: true,
	useCreateIndex: true,
	useUnifiedTopology: true,
	useFindAndModify: false,
});

const connection = mongoose.connection;
connection.once('open', () => {
	console.log('Mongoose connection opened!');
	app.emit('Mongoose ready');
});

const menuRouter = require('./routes/menu');

app.get('/', (req, res) => {
	res.json('Welcome to Brutriton API!');
});

app.use('/menus', menuRouter);

module.exports.app = app;
