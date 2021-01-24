const mongoose = require('mongoose');
const subMenu = require('./subMenu.model');

const schema = mongoose.Schema;

const diningHallSchema = new schema({
  name: {
    type: String,
    required: true,
  },
  submenus: {
    type: [subMenu.SubMenu.schema],
    required: true
  }
})

const DiningHall = mongoose.model('DiningHall', diningHallSchema);

module.exports.DiningHall = DiningHall;
