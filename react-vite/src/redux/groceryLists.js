// imports
import { csrfFetch } from "./csrf";

// action types
const ADD = 'groceryLists/ADD';

// action creators

const add = list => ({
    type: ADD,
    list,
});

//  thunks

// creates a grocerylist for all new users, future implementation will allow for multiple lists
export const thunkAddList = () => async dispatch => {
    const response = await csrfFetch('/api/lists/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if(response.ok) {
        const list = await response.json();
        dispatch(add(list));
    } else {
        return response;
    }
}

// initial state
const initialState = {usersGroceryLists: {}};

// reducer
function groceryListsReducer(state = initialState, action) {
    switch (action.type) {
        case ADD: {
            return {
                ...state,
                usersGroceryLists: {
                    ...state.usersGroceryLists,
                    [action.list.id]: action.list,
                },
            };
        }
        default:
            return state;
    }
}

export default groceryListsReducer;
