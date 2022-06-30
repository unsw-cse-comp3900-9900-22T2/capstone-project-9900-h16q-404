import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import { Button } from 'antd';
import { useNavigate } from 'react-router-dom';

/**
 * Make the Login Button a separate component
 * It can be revoked everywhere the page needs a login button
 * @returns the button component
 */

export default function LogoutButton() {
  let navigate = useNavigate();
  const func = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('token');
    window.location.reload(true);
  };
  return (
    <>
      <Button onClick={func}>Log out</Button>
    </>
  );
}
