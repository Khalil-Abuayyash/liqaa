import React, { useState } from 'react';
import axios from 'axios';

const BookInterview = () => {
    const [interviewData, setInterviewData] = useState({
        interviewer: '',
        interviewee: '',
        scheduled_date: '',
        start_time: '',
        end_time: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setInterviewData({
            ...interviewData,
            [name]: value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://127.0.0.1:8080/api/interviews/', interviewData)
            .then(response => {
                console.log('Interview booked successfully:', response.data);
            })
            .catch(error => {
                console.error('Error booking interview:', error);
            });
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Book an Interview</h3>
            <input
                type="text"
                name="interviewer"
                placeholder="Interviewer"
                value={interviewData.interviewer}
                onChange={handleChange}
            />
            <input
                type="text"
                name="interviewee"
                placeholder="Interviewee"
                value={interviewData.interviewee}
                onChange={handleChange}
            />
            <input
                type="date"
                name="scheduled_date"
                value={interviewData.scheduled_date}
                onChange={handleChange}
            />
            <input
                type="time"
                name="start_time"
                value={interviewData.start_time}
                onChange={handleChange}
            />
            <input
                type="time"
                name="end_time"
                value={interviewData.end_time}
                onChange={handleChange}
            />
            <button type="submit">Submit</button>
        </form>
    );
};

export default BookInterview;
