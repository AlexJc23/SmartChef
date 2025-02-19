import { csrfFetch } from "./csrf";

const LOAD = 'recipes/LOAD';

const load = list => ({
    type: LOAD,
    list,
});

export const thunkFetchRecipes = (ingredients) => async dispatch => {
    const response = await csrfFetch('/api/recipes/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients }),
    });

    if(response.ok) {
        const list = await response.json();
        dispatch(load(list));
    }
}


const initialState = {
    generatedRecipe: {},
};

function recipesReducer(state = initialState, action) {
    switch (action.type) {
        case LOAD: {
            return {
                ...state,
                generatedRecipe: action.list,
            };
        }
        default:
            return state;
    }
}


export default recipesReducer;
