import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CreateAvailability from './components/CreateAvailability';
import AvailabilityList from './components/AvailabilityList';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/create_availability" element={<CreateAvailability />} />
                <Route path="/availability_list" element={<AvailabilityList />} />
            </Routes>
        </Router>
    );
};

export default App;