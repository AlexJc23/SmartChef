// imports
import { csrfFetch } from "./csrf";

// action types
const ADD = 'items/ADD';
const ADDTOLIST = 'items/ADDTOLIST';
const REMOVEFROMLIST = 'items/REMOVEFROMLIST';

// action creators
const add = item => ({
    type: ADD,
    item,
});


const addToList = (list_id, item_name) => ({
    type: ADDTOLIST,
    list_id,
    item_name,
});

const removeFromList = (list_id, item_id) => ({
    type: REMOVEFROMLIST,
    list_id,
    item_id,
});


// thunks

// add item into db
export const thunkAddItem = (item) => async dispatch => {
    const response = await csrfFetch('/api/items/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
    });

    if(response.ok) {
        const item = await response.json();
        dispatch(add(item));
    } else {
        return response;
    }
}

// add item to grocery list
export const thunkAddItemToList = (list_id, item_name) => async dispatch => {
    const response = await csrfFetch(`/api/items/associate/${list_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ item: item_name }),
    });

    if(response.ok) {
        const item = await response.json();
        dispatch(addToList(list_id, item));
    } else {
        return response;
    }
}

// remove item from grocery list
export const thunkRemoveItemFromList = (list_id, item_id) => async dispatch => {
    const response = await csrfFetch(`/api/items/remove/${list_id}/${item_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if(response.ok) {
        dispatch(removeFromList(list_id, item_id));
    } else {
        return response;
    }
}

// initial state
const initialState = {items: {}, groceryLists: {}};

// reducer
const itemsReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD:
            return {
                ...state,
                items: {
                    ...state.items,
                    [action.item.id]: action.item
                }
            }
        case ADDTOLIST:
            return {
                ...state,
                groceryLists: {
                    ...state.groceryLists,
                    [action.list_id]: {
                        ...state.groceryLists[action.list_id],
                        [action.item_name]: action.item_name,
                    }
                }
            }
        case REMOVEFROMLIST: {
            const list = state.groceryLists[action.list_id];
            delete list[action.item_id];
            return {
                ...state,
                groceryLists: {
                    ...state.groceryLists,
                    [action.list_id]: list,
                }
            }
        }
        default:
            return state;
    }
}


export default itemsReducer;
