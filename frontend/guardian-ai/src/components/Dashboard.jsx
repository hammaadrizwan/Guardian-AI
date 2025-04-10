import React, {useState, useEffect} from 'react';
import NavBar from './Navbar';
import Footer from './Footer';
import image from '../assets/images/graph.png'

function Dashboard() {
    const userDetails = JSON.parse(localStorage.getItem('userDetails'));

    // if (!userDetails || !userDetails.name) {
    //     // Redirect to login page or display message
    //     return (<div className='error-404'><p className='error-404-text'>404 Bad Request</p></div>);
    // }

    return (
        <>
        <NavBar />
        <div className='VALUE-PROP'>
            <div className='frame'>
                <div className='text-wrapper'>Welcome, Arkhash</div>
            </div>

            <div className='GRID'>
                <div className='incident-pred-card'>
                    <div className='latest-incident-pred'>
                        <div className='latest-incident-bg'>
                            <div className='latest-incident-text-cover'>
                                <div className='latest-incident-val'>
                                    <p>01/03/24</p>
                                </div>

                                <div className='latest-incident-text'>
                                    <span className='latest-incident-span'>
                                        Latest
                                    </span>
                                    <br></br>
                                    <span className='latest-incident-span'>
                                        Incident Was
                                    </span>
                                    <span className='latest-incident-extra-span'/>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className='frame-2'>
                        <div className='total-incidents-over-wrapper'>
                            <div className='total-incidents-over'>
                                Total Incidents Over Time
                            </div>
                        </div>

                        <div className='image-wrapper'>
                            <img className='image' alt='Image' src={image} />
                        </div>
                    </div>
                </div>

                <div className='left-wrapper'>
                    <div className='left'>
                        <div className='summary-of-incidents-wrapper'>
                            <p className='summary-of-incidents'>
                                Summary of Incidents by Location
                            </p>
                        </div>

                        <div className='left-2'>
                            <div className='component-2'>
                                <div className='first-location'>
                                    Colombo, Sri Lanka
                                </div>
                                <div className='text-wrapper-3'>20</div>
                            </div>

                            <div className='component-3'>
                                <div className='second-location'>
                                    Gampaha, Sri Lanka
                                </div>
                                <div className='text-wrapper-4'>18</div>
                            </div>

                            <div className='component-4'>
                                <div className='third-location'>
                                    Jaffna, Sri Lanka
                                </div>
                                <div className='text-wrapper-5'>7</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className='GRID-2'>
                <div className='group'>
                    <div className='div-wrapper'>
                        <div className='text-wrapper-6'>
                            Image Captured
                        </div>
                    </div>

                    <div className='component-5'>
                        <img 
                        src="https://security-detection-images.s3.ap-south-1.amazonaws.com/images/09_04_2025_23_34_21.jpg"
                        alt="Detected Image"
                        className='image-2'
                        />
    
                    </div>


                    <div className='download-image-now-wrapper'>
                        <div className='download-image-now'>Download Image Now</div>
                    </div>
                </div>

                <div className='component-wrapper'>
                    <div className='component-6'>
                        <div className='overlap-group-2'>
                            <div className='rectangle' />

                            <div className='first-date'>28.02.2025</div>

                            <div className='second-date'>01.03.2025</div>

                            <div className='third-date'>05.03.2025</div>

                            <div className='element'>{""}</div>

                            <div className='rectangle-wrapper'>
                                <div className='rectangle-2' />
                            </div>

                            <div className='table-heading'>Date</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}

export default Dashboard;