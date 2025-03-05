import Cookies from "js-cookie";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkFetchRecipes, thunkAddRecipe } from "../../redux/recipes";

const Recipe = () => {
    const dispatch = useDispatch();
    const [ingredients, setIngredients] = useState('');
    const [isLoaded, setIsLoaded] = useState(false);
    const [hasAddedRecipe, setHasAddedRecipe] = useState(false);
    const generatedRecipe = useSelector(state => state.recipe.generatedRecipe);

    useEffect(() => {
        setIngredients(Cookies.get('ingredients'));
    }, []);

    useEffect(() => {
        if (ingredients) {
            dispatch(thunkFetchRecipes({ingredients}));
            setIsLoaded(true);
        }
    }, [ingredients, dispatch]);

    useEffect(() => {
        if (generatedRecipe?.name && !hasAddedRecipe) {
            dispatch(thunkAddRecipe(generatedRecipe));
            setHasAddedRecipe(true);
        }
    }, [generatedRecipe, dispatch, hasAddedRecipe]);


    console.log("Generated Recipe:", generatedRecipe);


    return !isLoaded ? (
        <h1>Hello World!</h1>
    ) : (
        <div>
            <div>
                <p>Search bar here</p>
                <div>
                    <h1>{generatedRecipe?.name}</h1>
                    <p>{generatedRecipe?.ingredients}</p>
                </div>
            </div>
        </div>
    );
};

export default Recipe;
