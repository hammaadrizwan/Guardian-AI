import React, {useState, useEffect} from "react";
import logo from '../assets/images/logo_with_name.png';
import {Routes, Route} from "react-router-dom";

function NavBar() {
    const [loginSuccess, setlLoginSuccess] = useState('');
    const userDetails = JSON.parse(localStorage.getItem('userDetails'));

    useEffect(() => {
        if (userDetails && userDetails.name !== "") {
            setlLoginSuccess("Success");
        }
    }, [userDetails]); // this will run when userDetails changes

    function onLogout() {
        localStorage.setItem('userDetails', JSON.stringify({name: ""}));
        setlLoginSuccess("");
    }

    return  (
        <nav className='nav'>
            <img className="nav-image" src={logo} alt="guardian-ai-logo"  style={{ width: '10%', height: 'auto' }} />
            <ul className="nav-list">
                <li><a href="/" className='hidden nav-home md:flex hover:font-bold'>Home</a></li>
                <li><a href="/contact" className='hidden nav-contact md:flex hover:font-bold'>Contact</a></li>
                {
                    loginSuccess === "Success" ?
                    <a href="/login" className='ml-3 nav-login-button hover:animate-pulse' onClick={onLogout}>Logout</a>
                    :
                    <a href="/login" className='ml-3 nav-login-button hover:animate-pulse'>Login</a>
                }
            </ul>
        </nav>
    )
}

export default NavBar;