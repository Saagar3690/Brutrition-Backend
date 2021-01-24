const mongoose = require('mongoose');
const item = require('./item.model');

const schema = mongoose.Schema;

const subMenuSchema = new schema({
  name: {
    type: String,
    required: true,
  },
  items: {
    type: [item.Item.schema],
    required: true
  }
})

const SubMenu = mongoose.model('SubMenu', subMenuSchema);

module.exports.SubMenu = SubMenu;
