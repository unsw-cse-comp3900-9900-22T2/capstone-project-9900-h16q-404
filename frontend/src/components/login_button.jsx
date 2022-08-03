import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'antd';

/**
 * Make the Login Button a separate component
 * It can be revoked everywhere the page needs a login button
 * @returns the button component
 */

export default function LoginButton() {
  return (
    <>
      <Link to='/login'>
        <Button type='primary'>Login</Button>
      </Link>
    </>
  );
}
