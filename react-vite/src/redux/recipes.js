// imports
import { csrfFetch } from "./csrf";

// action types
const LOAD = 'recipes/LOAD';
const ADD = 'recipes/ADD';
const FAVORITE = 'recipes/FAVORITE';
const REMOVEFAVORITE = 'recipes/REMOVEFAVORITE';

// action creators
const load = list => ({
    type: LOAD,
    list,
});

const add = recipe => ({
    type: ADD,
    recipe,
});

const favorite = recipe_id => ({
    type: FAVORITE,
    recipe_id,
});

const removeFavorite = recipe_id => ({
    type: REMOVEFAVORITE,
    recipe_id,
});


// thunks

// Grab generated Recipe
export const thunkFetchRecipes = (ingredients) => async dispatch => {
    const response = await csrfFetch('/api/recipe/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients }),
    });

    if(response.ok) {
        const list = await response.json();
        dispatch(load(list));
    } else {
        return response;
    }

}

// add recipe into db
export const thunkAddRecipe = (recipe) => async dispatch => {
    try {
        const response = await csrfFetch('/api/recipe/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ recipe }),
        });

        if (response.ok) {
            const newRecipe = await response.json();
            dispatch(add(newRecipe));
            return newRecipe;
        } else {
            const error = await response.json();
            return error;
        }
    } catch (err) {
        console.error('Error:', err);
        return { error: err.message };
    }
}

// user can add recipe to favorites with recipe_id
export const thunkFavoriteRecipe = (recipe_id) => async dispatch => {
    const response = await csrfFetch(`/api/recipes/favorite/${recipe_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if(response.ok) {
        const recipe = await response.json();
        dispatch(favorite(recipe.id));
    } else {
        return response;
    }
}

// user can remove recipe from favorites with recipe_id
export const thunkRemoveFavorite = (recipe_id) => async dispatch => {
    const response = await csrfFetch(`/api/recipes/remove/${recipe_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if(response.ok) {
        dispatch(removeFavorite(recipe_id));
    }
}

// initial state
const initialState = {
    generatedRecipe: {},
    favoriteRecipes: {},
};


// reducer
function recipesReducer(state = initialState, action) {
    switch (action.type) {
        case LOAD: {
            return {
                ...state,
                generatedRecipe: action.list,
            };
        }
        case ADD: {
            return {
                ...state,
                generatedRecipe: action.recipe,
            };
        }
        case FAVORITE: {
            return {
                ...state,
                favoriteRecipes: {
                    ...state.favoriteRecipes,
                    [action.recipe_id]: action.recipe_id,
                },
            };
        }
        case REMOVEFAVORITE: {
            const newState = { ...state };
            delete newState.favoriteRecipes[action.recipe_id];
            return newState;
        }
        default:
            return state;
    }
}


export default recipesReducer;
