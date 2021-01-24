const mongoose = require('mongoose');
const diningHall = require('./diningHall.model');


const schema = mongoose.Schema;

const menuSchema = new schema({
  diningHalls: {
    type: [diningHall.DiningHall.schema],
    required: true,
  },
  created: {
    type: Date,
    required: true
  }
})

const Menu = mongoose.model('Menu', menuSchema);

module.exports.Menu = Menu;
