import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AvailabilityList = () => {
    const [availability, setAvailability] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8080/api/availability/') 
            .then(response => {
                setAvailability(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the availability!', error);
            });
    }, []);

    return (
        <div>
            <h2>Available Slots</h2>
            <ul>
                {availability.map(slot => (
                    <li key={slot.id}>
                        {slot.available_date} from {slot.start_time} to {slot.end_time}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default AvailabilityList;
