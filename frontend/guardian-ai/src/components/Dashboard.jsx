import React, { useState, useEffect } from 'react';
import NavBar from './Navbar';
import Footer from './Footer';
import Plot from 'react-plotly.js';
import axios from 'axios';
import Papa from 'papaparse';

function Dashboard() {
    const userDetails = JSON.parse(localStorage.getItem('userDetails'));

    // State to store chart data
    const [chartData, setChartData] = useState({ dates: [], counts: [] });
    const [latestDate, setLatestDate] = useState('');
    const [locationCounts, setLocationCounts] = useState({});
    const [incidentList, setIncidentList] = useState([]);
    const [selectedImage, setSelectedImage] = useState('');

    // Function to fetch and process CSV data
    const fetchData = async () => {
        try {
            const csvUrl = `https://security-detection-images.s3.ap-south-1.amazonaws.com/detection_logs.csv?_=${new Date().getTime()}`;
            const response = await axios.get(csvUrl, {
                headers: {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                },
            });
    
            const parsedData = Papa.parse(response.data, {
                header: true,
                skipEmptyLines: true,
            }).data;
    
            // Count incidents per day
            const incidentCounts = {};
            const locationCountsTemp = {};
    
            parsedData.forEach(row => {
                const date = row.date; // "dd-mm-yyyy"
                const location = row[" location"]?.trim();
                
                if (date) {
                    incidentCounts[date] = (incidentCounts[date] || 0) + 1;
                }
                if (location) {
                    locationCountsTemp[location] = (locationCountsTemp[location] || 0) + 1;
                }
            });
    
            // Ensure "01-04-2025" is included with 0 count if missing
            const baseDate = "01-04-2025";
            if (!incidentCounts[baseDate]) {
                incidentCounts[baseDate] = 0;
            }
    
            // Get dates and sort them properly
            const dates = Object.keys(incidentCounts).sort((a, b) => {
                const [dayA, monthA, yearA] = a.split("-").map(Number);
                const [dayB, monthB, yearB] = b.split("-").map(Number);
                return new Date(yearA, monthA - 1, dayA) - new Date(yearB, monthB - 1, dayB);
            });
    
            const counts = dates.map(date => incidentCounts[date]);
            setChartData({ dates, counts });

            if (dates.length > 0) {
                const lastDate = dates[dates.length - 1]; // '14-04-2025'
                const [day, month, year] = lastDate.split('-');
                const formattedLatestDate = `${day}/${month}/${year.slice(-2)}`; // '14/04/25'
                setLatestDate(formattedLatestDate);
            }

            // Create a list of incidents with combined dateTime and imageLink
            const allIncidents = parsedData
            .map(row => {
                const date = row.date?.trim(); // "dd-mm-yyyy"
                const time = row[" time"]?.trim(); // "hh:mm:ss"
                const image = row[" image_link"]?.trim();
                if (date && time && image) {
                    return {
                        dateTime: `${date} ${time}`,
                        image
                    };
                }
                return null;
            })
            .filter(Boolean);

            // Sort by newest dateTime
            allIncidents.sort((a, b) => {
                const [d1, t1] = a.dateTime.split(" ");
                const [d2, t2] = b.dateTime.split(" ");
                const [dayA, monthA, yearA] = d1.split("-").map(Number);
                const [dayB, monthB, yearB] = d2.split("-").map(Number);
                const dateA = new Date(yearA, monthA - 1, dayA, ...t1.split(":").map(Number));
                const dateB = new Date(yearB, monthB - 1, dayB, ...t2.split(":").map(Number));
                return dateB - dateA; // latest first
            });

            // Set image from most recent record
            if (allIncidents.length > 0) {
                setSelectedImage(allIncidents[0].image);
            }
            locationCountsTemp["Colombo,Sri Lanka"] = 0; // Ensure this date is included with 0 count
            setIncidentList(allIncidents);
            setLocationCounts(locationCountsTemp); // Set location data
        } catch (error) {
            console.error('Error fetching or parsing CSV:', error);
        }
    };

    // Fetch data on mount and every minute
    useEffect(() => {
        fetchData(); // Initial fetch
        const interval = setInterval(fetchData, 10 * 1000); // Refresh every 10 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, []);

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
                                <p>{latestDate || ''}</p>
                            </div>

                                <div className='latest-incident-text'>
                                <div className='latest-incident-text'>
                                <div className='latest-incident-span' style={{ lineHeight: '1.3' }}>
                                    Recent
                                </div>
                                <div className='latest-incident-span' style={{ lineHeight: '1.1' }}>
                                    Case Log
                                </div>
                                </div>

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
                            <Plot
                                data={[
                                    {
                                        x: chartData.dates,
                                        y: chartData.counts,
                                        type: 'scatter',
                                        mode: 'lines+markers',
                                        line: { color: '#FF5733', width: 2 },
                                        marker: { size: 6 },
                                        fill: 'tozeroy',
                                        fillcolor: 'rgba(255, 87, 51, 0.3)', // Semi-transparent orange
                                        hovertemplate: '<b>Date</b>: %{x}<br><b>Incidents</b>: %{y}<extra></extra>',
                                    },
                                    ...chartData.dates.map((date, index) => ({
                                        x: [date, date],
                                        y: [0, chartData.counts[index]],
                                        mode: 'lines',
                                        line: {
                                            color: 'rgba(200, 200, 200, 0.5)', // Light gray
                                            width: 1,
                                            dash: 'dot',
                                        },
                                        hoverinfo: 'skip',
                                        showlegend: false,
                                    })),
                                ]}
                                layout={{
                                    autosize: true,
                                    plot_bgcolor: 'rgba(0,0,0,0)',
                                    paper_bgcolor: 'rgba(0,0,0,0)',
                                    margin: { t: 10, b: 10, l: 10, r: 10 },
                                    xaxis: {
                                        showgrid: false,
                                        zeroline: false,
                                        visible: false,
                                    },
                                    yaxis: {
                                        showgrid: false,
                                        zeroline: false,
                                        visible: false,
                                    },
                                    showlegend: false,
                                }}
                                style={{ width: '100%', height: '300px', marginTop: '10px' }}
                                config={{
                                    responsive: true,
                                    displayModeBar: false,
                                    displaylogo: false,
                                    modeBarButtonsToRemove: ['sendDataToCloud'],
                                }}
                            />
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
                            {Object.entries(locationCounts).map(([location, count], index) => {
                                const [place, country] = location.split(',').map(part => part.trim());

                                return (
                                    <div key={index} className={`component-${index + 2}`}>
                                        <div className={`location-${index + 1}`}>
                                            <span>{place}</span>
                                            <br />
                                            <span style={{ fontSize: 30, fontWeight: 20 }}>{country}</span>
                                        </div>
                                        <div className={`text-wrapper-${index + 3}`}>{count}</div>
                                    </div>
                                );
                            })}
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
                            src={selectedImage} 
                            alt="Detected Image" 
                            className="image-2"
                        />
                    </div>

                    <div className='download-image-now-wrapper'>
                        <a href={selectedImage} download="incident-image">
                            Download Image Now
                        </a>
                    </div>
                </div>

                <div className='component-wrapper'>
                <p className="text-left mt-2">All Time Records</p>
                    <div className='component-6'>
                        <div className='table-container'>
                            <table className="incident-table">
                                <thead>
                                    <tr>
                                        {/* <th className="table-header-cell">Date & Time</th> */}
                                    </tr>
                                </thead>
                                <tbody>
                                    {incidentList.map((incident, index) => (
                                        <tr key={index} onClick={() => setSelectedImage(incident.image)} className="table-row">
                                            <td className="table-record-cell">{incident.dateTime}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    );
}

export default Dashboard;
