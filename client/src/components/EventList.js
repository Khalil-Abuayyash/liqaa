import React, { useEffect, useState } from 'react';
import { fetchEvents } from '../api';

const EventList = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const getEvents = async () => {
            try {
                const eventData = await fetchEvents();
                setEvents(eventData);
            } catch (error) {
                console.error('Error fetching events:', error);
            }
        };

        getEvents();
    }, []);

    return (
        <div>
            <h2>Upcoming Events</h2>
            <ul>
                {events.map((event) => (
                    <li key={event.id}>
                        {event.summary} - {new Date(event.start.dateTime).toLocaleString()}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default EventList;
