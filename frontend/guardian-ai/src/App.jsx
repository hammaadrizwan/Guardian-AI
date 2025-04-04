import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { Routes, Route, BrowserRouter} from 'react-router-dom';
import Index from './components/Index';
// import Login from './components/Login';
// import Contact from './components/Contact';
// import Dashboard from './components/Dashboard';

function App() {
  
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<Index />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;