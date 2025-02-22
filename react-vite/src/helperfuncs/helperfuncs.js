
import Cookies from 'js-cookie';



export const handleSearchChange = (e, setIngredients) => {
  const value = e.target.value;
  setIngredients(value);  // Update state
  Cookies.set('ingredients', value, { expires: 3 }); // Set cookie with 3-day expiry
};


export const handleKeyDown = (e, navigate) => {
    if (e.key === "Enter") {  // Check if Enter key is pressed
        e.preventDefault();  // Prevent default form submission
        navigate('/recipe');  // Navigate to /recipe
    }
};
