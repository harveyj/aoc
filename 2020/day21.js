module.exports = { _input, _ANSWER_1, _ANSWER_2};

function _1(md){return(
md`# Advent 2020 Day 21!`
)}

function _input(input) {
  return processInput(input);
}

function processInput(input) {
  function processFood(rawFood) {
    rawFood = rawFood.split(')')[0];
    let allergens = rawFood
      .split('(contains')[1]
      .split(',')
      .map(a => a.trim());
    let ingredients = rawFood
      .split('(')[0]
      .split(' ')
      .filter(a => a);
    return { ingredients, allergens };
  }
  return input.split('\n').map(processFood);
};

function genAllergensToRecipes(input) {
  let retMap = new Map();
  for (let [recipeIdx, recipe] of input.entries()) {
    for (let allergen of recipe.allergens) {
      let recipeList = retMap.get(allergen) || [];
      recipeList.push(recipeIdx);
      retMap.set(allergen, recipeList);
    }
  }
  return retMap;
}


function genIngredientsToRecipes(input)
{
  let retMap = new Map();
  for (let [recipeIdx, recipe] of input.entries()) {
    for (let ingredient of recipe.ingredients) {
      let recipeList = retMap.get(ingredient) || [];
      recipeList.push(recipeIdx);
      retMap.set(ingredient, recipeList);
    }
  }
  return retMap;
}


function intersect(a, b) {
  return new Set([...a].filter(x => b.has(x)));
}

function subtract(a, b) {
  return new Set([...a].filter(x => !b.has(x)));
}

function genAllAllergens(input)
{
  let retSet = new Set();
  for (let [recipeIdx, recipe] of input.entries()) {
    for (let allergen of recipe.allergens) {
      retSet.add(allergen);
    }
  }
  return retSet;
}

function genAllIngredients(input)
{
  let retSet = new Set();
  for (let [recipeIdx, recipe] of input.entries()) {
    for (let ingredient of recipe.ingredients) {
      retSet.add(ingredient);
    }
  }
  return retSet;
}


function allergenToPossibilities(allergen, exclusions, input) {
  let allergensToRecipes = genAllergensToRecipes(input);
  let possibleSet = new Set(
    input[allergensToRecipes.get(allergen)[0]].ingredients
  );
  possibleSet = subtract(possibleSet, new Set(exclusions));
  for (let recipeIdx of allergensToRecipes.get(allergen)) {
    let recipe = input[recipeIdx];
    possibleSet = intersect(possibleSet, new Set(recipe.ingredients));
  }
  return possibleSet;
}

function _GEN_ANSWER_1(input) {
  let allAllergens = genAllAllergens(input);
  let allergenToPossibleRecipes = new Map();
  let knownAllergens = new Map();
  for (let i = 0; i < 10; i++) {
    for (let allergen of allAllergens) {
      let results = Array.from(
        allergenToPossibilities(allergen, knownAllergens.keys(), input)
      );
      if (results.length == 1) {
        knownAllergens.set(results[0], allergen);
      }
    }
  }
  let total = 0;
  let allIngredients = genAllIngredients(input);
  let ingredientsToRecipes = genIngredientsToRecipes(input);
  for (let ingredient of allIngredients) {
    if (knownAllergens.has(ingredient)) {
      continue;
    }
    total += ingredientsToRecipes.get(ingredient).length;
  }
  return { knownAllergens, total };
}

function _ANSWER_1(input) {
  return _GEN_ANSWER_1(input).total;
}

function _ANSWER_2(input)
{
  let ANSWER_1 = _GEN_ANSWER_1(input);
  let allergenToIngredient = new Map(
    Array.from(ANSWER_1.knownAllergens, a => a.reverse())
  );

  return Array.from(ANSWER_1.knownAllergens.values())
    .sort()
    .map(a => allergenToIngredient.get(a))
    .join();
}
