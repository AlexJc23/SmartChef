import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import OpenModalMenuItem from "../Navigation/OpenModalMenuItem";
import LoginFormModal from "../LoginFormModal/LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import { handleSearchChange, handleKeyDown } from "../../helperfuncs/helperfuncs";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import Loading from "../Loading";


const HomePage = () => {
    const navigate = useNavigate();

    const [ingredients, setIngredients] = useState("");
    const [isLoaded, setIsLoaded] = useState(false);

    const user = useSelector(state => state.session.user);
    const load = false
    // Get ingredients from cookie on mount
    useEffect(() => {
        const cookieIngredients = Cookies.get('ingredients');
        if (cookieIngredients) {
            setIngredients(cookieIngredients);
            setIsLoaded(true);
        }
        setIsLoaded(true);
    }, []);



    return !isLoaded ? (<Loading />) : (
        <div className="flex flex-col items-center">
            <div className="flex flex-col items-center">
                <img className="max-h-100 mt-10" src="/4.svg" alt="SmartChef logo" />
                <p className="text-[1rem] max-w-100 mt-10 font-thin max-sm:text-xs w-[90%]">Got a fridge full of random stuff and no clue what to make? Don&apos;t worry—your next delicious meal is just a click away, powered by the magic of AI!</p>
            </div>
            <div>

                    <input
                        className="border-2 bg-gray-100 mt-10 px-3 py-2 rounded-tl-3xl rounded-bl-3xl w-80 max-w-[500px] shadow-xl max-sm:w-[90%] max-sm:rounded-3xl max-sm:px-1 max-sm:py-2 max-sm:text-xs"
                        type="text"
                        value={ingredients}
                        onChange={(e) => handleSearchChange(e, setIngredients)}
                        onKeyDown={e => handleKeyDown(e, navigate)}
                        placeholder="Place some ingredients..."
                    />
                    <button className="border-2 border-black text-white bg-[#5D59D9] rounded-tr-3xl rounded-br-3xl mt-10 px-3 py-2 bl-none shadow-xl cursor-pointer hover:bg-[#F24968] max-sm:hidden" onClick={() => navigate('/recipe')}>
                        Cook!
                    </button>

            </div>
            {!user ? (<div className="flex items-center text-xs mt-2">
                <p> If you&apos;re already part of the kitchen crew, </p>
                <OpenModalMenuItem
                    itemText=" Log In "
                    onItemClick={() => {}}
                    modalComponent={<LoginFormModal />}
                />
                <p> or </p>
                <OpenModalMenuItem
                    itemText=" Sign Up "
                    onItemClick={() => {}}
                    modalComponent={<SignupFormModal />}
                />
                <p> if not!</p>
            </div>) : (<button onClick={() => navigate('/dashboard') } className="mt-10 border-1 border-black rounded-xl px-4 py-2 cursor-pointer shadow-xl bg-[#F24968] hover:bg-[#5D59D9] hover:text-white active:bg-[#5D59D9] active:text-white max-sm:min-w-[100] max-sm:text-xs max-sm:mr-4">
                DashBoard
            </button>)}
        </div>
    );
};

export default HomePage;
