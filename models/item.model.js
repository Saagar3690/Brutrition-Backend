const mongoose = require('mongoose');

const schema = mongoose.Schema;

const nutrientSchema = new schema({
  val: {
    type: String,
    required: true,
  },
  dailyVal: {
    type: String,
    required: true,
  },
});

const nutritionInfoSchema = new schema({
  prodWebCodes: {
    type: [String],
    required: false,
  },
  servingSize: {
    type: String,
    required: false,
  },
  calories: {
    type: String,
    required: false,
  },
  fatCalories: {
    type: String,
    required: false,
  },
  totalFat: {
    type: {
      val: {
        type: String,
        required: true,
      },
      dailyVal: {
        type: String,
        required: true,
      },
    },
    required: false,
  },
  saturatedFat: {
    type: {
      val: {
        type: String,
        required: true,
      },
      dailyVal: {
        type: String,
        required: true,
      },
    },
    required: false,
  },
  transFat: {
    type: String,
    required: false,
  },
  cholesterol: {
    type: {
      val: {
        type: String,
        required: true,
      },
      dailyVal: {
        type: String,
        required: true,
      },
    },
    required: false,
  },
  sodium: {
    type: {
      val: {
        type: String,
        required: true,
      },
      dailyVal: {
        type: String,
        required: true,
      },
    },
    required: false,
  },
  totalCarbohydrate: {
    type: {
      val: {
        type: String,
        required: true,
      },
      dailyVal: {
        type: String,
        required: true,
      },
    },
    required: false,
  },
  dietaryFiber: {
    type: {
      val: {
        type: String,
        required: true,
      },
      dailyVal: {
        type: String,
        required: true,
      },
    },
    required: false,
  },
  sugars: {
    type: String,
    required: false,
  },
  protein: {
    type: String,
    required: false,
  },
  vitaminA: {
    type: String,
    required: false,
  },
  vitaminC: {
    type: String,
    required: false,
  },
  calcium: {
    type: String,
    required: false,
  },
  iron: {
    type: String,
    required: false,
  },
  ingredients: {
    type: String,
    required: false,
  },
  allergens: {
    type: String,
    required: false,
  }
})

const itemSchema = new schema({
  name: {
    type: String,
    required: true,
  },
  nutritionInfo: {
    type: nutritionInfoSchema,
    required: true,
  },
  mealType: {
    type: String,
    required: true
  }
})

const Item = mongoose.model('Item', itemSchema);
const NutritionInfo = mongoose.model('NutritionInfo', nutritionInfoSchema);
const Nutrient = mongoose.model('Nutrient', nutrientSchema);

module.exports.Item = Item;
module.exports.NutritionInfo = NutritionInfo;
module.exports.Nutrient = Nutrient;
