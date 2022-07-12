import React from 'react';
import { Button, message } from 'antd';
import { useNavigate } from 'react-router-dom';

/**
 * Make the Logout Button a separate component
 * It can be revoked everywhere the page needs a login button
 * @returns the button component
 */

export default function LogoutButton() {
  const navigate = useNavigate();
  const func = () => {
    // since we are storing more items in localStorage, using clear to remove all when logout.
    localStorage.clear();
    // improve: give some UI feedback when user logout
    message.success("Logout Successful!", 3)
      // and use navigate function to switch to main page instead
      .then(navigate("/"));
  };
  return (
    <>
      <Button onClick={func}>Log out</Button>
    </>
  );
}
