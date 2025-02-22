import { NavLink, useLocation } from "react-router-dom";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";
import { useState, useEffect } from "react";

function Navigation() {
  const location = useLocation();
  const path = location.pathname;
  const [isHome, setIshome] = useState(path === "/");

  useEffect(() => {
    setIshome(path === "/");
  }, [path])

  return !isHome ? (
    <ul>
      <li>
        <NavLink to="/">Home</NavLink>
      </li>
      <li>
        <ProfileButton />
      </li>
    </ul>
  ) : null;
}

export default Navigation;
