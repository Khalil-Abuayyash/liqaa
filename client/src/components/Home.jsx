import React from 'react';
import './Home.css';
import Sun from './Sun';
import Card from './Card';

const Home = () => {
  return (
    <>
      <Sun />
      <div className="home">
        <h1>Welcome to the Interview App!</h1>
        <p>
          This platform allows you to connect with others for interviews and
          discussions.
        </p>
        <p>Explore, share, and learn from each other.</p>
        <p>
          <strong>Get started today!</strong> Sign up or log in to join the
          community.
        </p>
        <div>
          <div className={'signupButton'}>
            <button>Sign Up</button>
            {/* <button>Learn More</button> */}
          </div>
        </div>
      </div>
      <div className={'cards'}>
        <Card title={'Peer'} content={'meet your colleage'} />
        <Card title={'Expert'} content={'meet your mentor'} />
        <Card title={'Company'} content={'meet your future company'} />
      </div>
    </>
  );
};

export default Home;
