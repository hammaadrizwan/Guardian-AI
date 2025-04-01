import React, {useState, useEffect} from 'react';
import './App.css';
import NavBar from './components/Navbar';
import Footer from './components/Footer';
import { Routes, Route, BrowserRouter} from 'react-router-dom';
import Login from './components/Login';

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route exact path="/" element={<Login />} />
                </Routes>
                <Footer />
            </BrowserRouter>
        </>
    );
}

export default App;