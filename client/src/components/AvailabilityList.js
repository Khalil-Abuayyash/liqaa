import React, { useEffect, useState } from 'react';
import { fetchAvailability } from '../api';

const AvailabilityList = () => {
    const [availability, setAvailability] = useState([]);

    useEffect(() => {
        const getAvailability = async () => {
            try {
                const data = await fetchAvailability();
                setAvailability(data);
            } catch (error) {
                console.error('Error fetching availability:', error);
            }
        };

        getAvailability();
    }, []);

    return (
        <div>
            <h2>Available Time Slots</h2>
            <ul>
                {availability.map((slot) => (
                    <li key={slot.id}>
                        {slot.available_date} from {slot.start_time} to {slot.end_time} ({slot.status})
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AvailabilityList;
