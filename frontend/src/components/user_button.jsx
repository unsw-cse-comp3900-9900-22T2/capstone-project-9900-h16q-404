import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, Dropdown,Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';

const menu = (
  <Menu
    items={[
      {
        key: '1',
        label: <Link to='/edit_profile'>Edit Profile</Link>,
      },
      {
        ket: '2',
        label: <Link to='/edit_sensitive_profile'>Edit Sensitive Profile</Link>,
      },
      {
        key: '3',
        label: <Link to='/edit_login_credential'>Edit Login Credentials</Link>,
      },
      {
        key: '4',
        label: <Link to='/my_ticket'>View Tickets</Link>,
      },
    ]}
  ></Menu>
);

/**
 * Make the User Button a separate component
 * It can be revoked everywhere the page needs a user button
 * @returns the button component
 */

export default function UserButton() {
  const navigate = useNavigate();
  const userPageLocation = '/user?userId=' + localStorage.getItem('userId');

  const userButtonOnClick = () => {
    navigate(userPageLocation);
  };

  return (
    // also store userId in localStorage
    <Dropdown.Button onClick={userButtonOnClick} overlay={menu} type='primary'>
      {localStorage.getItem('userIcon') === 'default' ||
      localStorage.getItem('userIcon') === 'null' ||
      localStorage.getItem('userIcon') === null ? (
        <Avatar size={24} icon={<UserOutlined />} />
      ) : (
        <Avatar size={24} src={localStorage.getItem('userIcon')} />
      )}
      {localStorage.getItem('username')}
    </Dropdown.Button>
  );
}
