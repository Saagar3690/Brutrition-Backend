const { app } = require('./app');
const { PORT } = require('./constants');

const port = process.env.PORT || PORT;

app.on('Mongoose ready', () => {
	app.listen(port, () => {
		console.log(`Server started on port ${port}!\n`);
	});
});
