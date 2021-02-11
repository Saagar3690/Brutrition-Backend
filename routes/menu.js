const express = require('express');

const menuRouter = express.Router();

let { Menu } = require('../models/menu.model');
let { DiningHall } = require('../models/diningHall.model');
let { SubMenu } = require('../models/subMenu.model');
let { Item, NutritionInfo } = require('../models/item.model');

/**
 * ----------------- GET (return information about objects) ----------------
 */

/**
 * Return a specific Menu by date
 */
menuRouter.route('/date').get(async (req, res) => {
	const date = req.body.date;
	if (!date)
		return res.status(400).json(`'date' not provided in request body`);

	try {
    let data = await Menu.findOne({
      created: date
    });
		res.json(data);
	} catch (err) {
		res.status(404).json(err);
	}
});

/**
 * ------------------------- POST (add new objects) -------------------------
 */

/**
 * Adds a new Menu object with a menu and date as provided in
 * the request's body.
 */
menuRouter.route('/').post(async(req, res) => {
  const { menu, created } = req.body

	if (!menu || !created) {
		return res
			.status(400)
			.json('Required menu / created data not in request body.');
	}

	let diningHalls = [];

	menu.diningHalls.forEach(async(diningHall) => {
		let submenus = [];

		diningHall.subMenus.forEach(async(subMenu) => {
			let items = [];

			subMenu.items.forEach(async(item) => {
				let newItem = {
					name: item.name,
					nutritionInfo: item.nutritionInfo,
					mealType: item.mealType
				}
				items.push(newItem);
			});
			submenus.push({
				name: subMenu.name,
				items: items,
			});
		});
		diningHalls.push({
			name: diningHall.name,
			submenus: submenus,
		});
	});

  const newMenu = new Menu({
    diningHalls: diningHalls,
    created: created
  })

  await newMenu
		.save()
		.then(() => {
			console.log(newMenu);
			res.json(newMenu);
		})
		.catch((err) => res.status(400).json(err));
});


/**
 * ------------------------- DELETE (remove objects) ------------------------
 */

/**
 * Deletes Menu with the date provided in the request's body.
 */
menuRouter.route('/').delete(async (req, res) => {
	const date = req.body.date;

	if (!date) {
		return res.status(400).json('Required date data not in request body.');
	}

	try {
    let menu = await Menu.findOne({
      created: date
    })

		if (!menu)
			return res.status(404).json('Could not find menu specified by date.');

		await menu.delete();
		console.log(`Successfully deleted menu: ${menu}`);
		res.json(`Deleted menu ${menu}`);
	} catch (err) {
		console.log('Error: ' + err);
		res.status(400).json(err);
	}
});

module.exports = menuRouter;
