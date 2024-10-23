import React from 'react';
import AvailabilityList from './components/AvailabilityList';
import InterviewBookingForm from './components/InterviewBookingForm';
import EventList from './components/EventList';

const App = () => {
    return (
        <div>
            <h1>Interview Preparation App</h1>
            <AvailabilityList />
            <InterviewBookingForm />
            <EventList />
        </div>
    );
};

export default App;