import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'antd';

/**
 * Make the User Button a separate component
 * It can be revoked everywhere the page needs a user button
 * @returns the button component
 */

export default function UserButton() {
  return (
    // WARNING: change self=true to userId=xxx after userId backend is done!
    // also store userId in localStorage
    <Link to='user?self=true'>
      <Button type='primary'>{localStorage.getItem('username')}</Button>
    </Link>
  );
}
