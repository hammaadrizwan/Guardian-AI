import React from 'react';
import logo from '../assets/images/logo_with_name.png';

function Footer() {
    return (
        <footer className='footer'>
            <img clssName='footer-image' src={logo} alt='guardian-ai-logo' />
            <p className='ml-20 footer-text'>
                COLOMBO | SRI LANKA
            </p>
        </footer>
    )
}

export default Footer;