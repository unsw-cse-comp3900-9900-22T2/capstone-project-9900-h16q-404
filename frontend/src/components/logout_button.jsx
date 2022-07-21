import React from 'react';
import { Button } from 'antd';

/**
 * Make the Logout Button a separate component
 * It can be revoked everywhere the page needs a login button
 * @returns the button component
 */

export default function LogoutButton() {
  const func = () => {
    // since we are storing more items in localStorage, using clear to remove all when logout.
    localStorage.clear();
    window.location.reload();
  };
  return (
    <>
      <Button onClick={func}>Log out</Button>
    </>
  );
}
