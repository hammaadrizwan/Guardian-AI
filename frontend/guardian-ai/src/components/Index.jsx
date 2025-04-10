import React from 'react'
import '../App.css'
import Hero from './Index/Hero.jsx'
import Info from './Index/Info.jsx'
import Navbar from './Navbar'
import Footer from './Footer'

import {Routes,Route} from 'react-router-dom'
/* Add the navbar hero team contacts and footer here */
function Index() {
  return (
    <>
      <Navbar />
      <Hero />

    </>
  )
}

export default Index