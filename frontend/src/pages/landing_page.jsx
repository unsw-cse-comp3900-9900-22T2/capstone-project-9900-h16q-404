import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'antd';

export default function LandingPage () {
  return (
    <div className='App'>
      <div>Landing Page</div>
      <Link to="login">
        <Button type='primary'>Login</Button>
      </Link>
      <Button>Register</Button>
    </div>
  )
}