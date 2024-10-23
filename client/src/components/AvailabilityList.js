import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AvailabilityList = () => {
    const [availabilities, setAvailabilities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAvailabilities = async () => {
            try {
                const response = await axios.get('https://127.0.0.1:8080/api/calendarapi/availability/');
                setAvailabilities(response.data);
                setLoading(false);
            } catch (err) {
                setError('Error fetching availabilities');
                setLoading(false);
            }
        };

        fetchAvailabilities();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div>
            <h1>Availability List</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Available Date</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {availabilities.map((availability) => (
                        <tr key={availability.id}>
                            <td>{availability.id}</td>
                            <td>{availability.user}</td>
                            <td>{availability.available_date}</td>
                            <td>{availability.start_time}</td>
                            <td>{availability.end_time}</td>
                            <td>{availability.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AvailabilityList;