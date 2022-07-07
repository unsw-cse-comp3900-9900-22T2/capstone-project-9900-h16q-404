import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'antd';

/**
 * Make the Register Button a separate component
 * It can be revoked everywhere the page needs a register button
 * @returns the button component
 */

export default function RegisterButton () {
  return (
    <Link to='/register'>
      <Button>Register</Button>
    </Link>
  )
}