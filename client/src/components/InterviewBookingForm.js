import React, { useState } from 'react';
import { createInterview } from '../api';

const InterviewBookingForm = () => {
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

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createInterview(interviewData);
            alert('Interview successfully booked!');
        } catch (error) {
            console.error('Error booking interview:', error);
            alert('Failed to book interview.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Book an Interview</h2>
            <label>
                Interviewer:
                <input
                    type="text"
                    name="interviewer"
                    value={interviewData.interviewer}
                    onChange={handleChange}
                />
            </label>
            <label>
                Interviewee:
                <input
                    type="text"
                    name="interviewee"
                    value={interviewData.interviewee}
                    onChange={handleChange}
                />
            </label>
            <label>
                Date:
                <input
                    type="date"
                    name="scheduled_date"
                    value={interviewData.scheduled_date}
                    onChange={handleChange}
                />
            </label>
            <label>
                Start Time:
                <input
                    type="time"
                    name="start_time"
                    value={interviewData.start_time}
                    onChange={handleChange}
                />
            </label>
            <label>
                End Time:
                <input
                    type="time"
                    name="end_time"
                    value={interviewData.end_time}
                    onChange={handleChange}
                />
            </label>
            <button type="submit">Book Interview</button>
        </form>
    );
};

export default InterviewBookingForm;
