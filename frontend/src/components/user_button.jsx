import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, Dropdown } from 'antd';

const menu = (
  <Menu
    items={[
      {
        key:'1',
        label: (<Link to='/edit_profile'>Edit Profile</Link>)
      },
      {
        key:'2',
        label:(<Link to='/edit_login_credential'>Edit Login Credentials</Link>)
      }
    ]}  
  >
  </Menu>
);

/**
 * Make the User Button a separate component
 * It can be revoked everywhere the page needs a user button
 * @returns the button component
 */

export default function UserButton() {
  const navigate = useNavigate();
  const userPageLocation = "/user?userId="+localStorage.getItem('userId');

  const userButtonOnClick = () => {
    navigate(userPageLocation)
  }

  return (
    // also store userId in localStorage
    <Dropdown.Button onClick={userButtonOnClick} overlay={menu} type="primary">{localStorage.getItem('username')}</Dropdown.Button>
  );
}
