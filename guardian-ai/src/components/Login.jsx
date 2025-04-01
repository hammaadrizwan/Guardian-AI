import React, {useState} from "react";
import image from '../assets/images/loginImage.jpg';
import '../App.css';
import Navbar from "./Navbar";
import Footer from "./Footer";

function Login() {
    const [loginType, setLoginType] = useState('login');
    const [loginSuccess, setLoginSuccess] = useState('');
    const [passwordError, setPasswordError] = useState('');
    const [error, setError] = useState('');
    const [userCredentials, setUserCredentials] = useState({});

    function handleCredentials(e) {
        setError("");
        setPasswordError("");
        setUserCredentials({ ...userCredentials, [e.target.name]: e.target.value });
    }

    function handleLogin(e) {
        e.preventDefault();
        
        // Dummy user credentials (accept anything entered)
        const dummyUser = {
            email: userCredentials.email,
            password: userCredentials.password,
            uid: "dummyUID1234", // Placeholder user ID
            name: "Guest User" // Placeholder name
        };
        
        // Store user details in local storage
        localStorage.setItem('userDetails', JSON.stringify(dummyUser));
        
        console.log("User logged in:", dummyUser);
        setLoginSuccess("Success"); // Set login success message
    }

    return (
        <>
        <Navbar />
        <section className="login">
            <div className='xl:pt-28 xl:pb-32 login-items'>
                <div className='hidden lg:flex login-left'>
                    <img className='login-image' src={image} alt='' />
                </div>
                <div className='login-right'>
                    <form className='xl:mr-10 lg:mr-10 login-right-info'>
                        <div className='login-right-info-title'>
                            <h1>Welcome</h1>
                        </div>
                        <div className='login-right-info-input'>
                            <input onChange={(e) => { handleCredentials(e) }} className='login-right-info-input-field' placeholder='Enter your Email' type='text' name="email" />
                            <input onChange={(e) => { handleCredentials(e) }} className='login-right-info-input-field' placeholder='Enter your password' type='password' name="password" />
                        </div>
                        <div className='login-right-info-input-submit'>
                            {
                                loginSuccess == "" ? (
                                    <input onClick={(e) => { handleLogin(e) }} id="login-bg-input" type="submit" value="Login" className="contact-button hover:drop-shadow-2xl " />
                                ) : (
                                    <div className='bg'>
                                        <a href='/dashboard' id='dashboard-login-bg-input' className='contact-button-dashboard hover:drop-shadow-2x1'>Dashboard</a>
                                    </div>
                                )
                            }
                        </div>
                    </form>
                </div>
                
                {/* <div className='self-stretch text-center justify-start text-neutral-700 text-base font-normal'>Create your account now</div> */}
            </div>
        </section>
        {/* <Footer /> */}
        </>
    );
}

export default Login;