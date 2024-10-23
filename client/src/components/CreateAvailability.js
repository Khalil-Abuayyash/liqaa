import React, { useState } from 'react';
import axios from 'axios';

const CreateAvailability = () => {
    const [userId, setUserId] = useState(''); // Assuming you need to capture the user ID
    const [availableDate, setAvailableDate] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        const availabilityData = {
            user: userId,  // Add user ID to the data object
            available_date: availableDate,
            start_time: startTime,
            end_time: endTime
        };

        if (startTime >= endTime) {
            setMessage("End time must be after start time.");
            return;
        }

        // Post the data to the correct endpoint
        axios.post('https://127.0.0.1:8080/availability/', availabilityData)
            .then(response => {
                console.log('Availability created:', response.data);
                setMessage("Availability created successfully!");
                setUserId('');  // Reset userId
                setAvailableDate('');
                setStartTime('');
                setEndTime('');
            })
            .catch(error => {
                console.error('There was an error creating the availability!', error);
                setMessage("Error creating availability: " + error.response?.data?.error || error.message);
            });
    };

    return (
        <div>
            <h1>Create Availability</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    User ID:
                    <input
                        type="text"
                        value={userId}
                        onChange={e => setUserId(e.target.value)}
                        required
                    />
                </label>
                <label>
                    Available Date:
                    <input
                        type="date"
                        value={availableDate}
                        onChange={e => setAvailableDate(e.target.value)}
                        required
                    />
                </label>
                <label>
                    Start Time:
                    <input
                        type="time"
                        value={startTime}
                        onChange={e => setStartTime(e.target.value)}
                        required
                    />
                </label>
                <label>
                    End Time:
                    <input
                        type="time"
                        value={endTime}
                        onChange={e => setEndTime(e.target.value)}
                        required
                    />
                </label>
                <button type="submit">Create Availability</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default CreateAvailability;
