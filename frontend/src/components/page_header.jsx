import React, { useEffect, useState } from 'react';
import { Layout } from 'antd';
import { Link } from 'react-router-dom'
import logo from '../static/picacg.jpeg';
import LoginButton from '../components/login_button';
import UserButton from '../components/user_button';
import LogoutButton from '../components/logout_button';
import RegisterButton from '../components/register_button';
import SearchInput from './search_input';
import './page_header.css'

const { Header } = Layout;

export default function PageHeader() {
  const [username, setUsername] = useState('');
  // fix: add a [] in useEffect hook
  useEffect(()=>{
    setUsername(localStorage.getItem('username'));
  }, []);
  return (
    <Header
      style={{
        position: 'fixed',
        zIndex: 1,
        width: '100%',
      }}
    >
      <div
        style={{
          float: 'left',
          height: '100%',
          display: 'flex',
          flexDirection: 'row',
          alignContent: 'center',
          justifyContent: 'center',
          textAlign: 'center',
        }}
      >
        <Link to="/">
          <img
            src={logo}
            alt='Logo'
            style={{ width: '45px', height: '45px', marginRight: '5px' }}
          />
        </Link>
        <h1 style={{ color: 'white', fontSize: 'bold', marginRight: '15px' }}>
          LiveKnight
        </h1>
        <div style={{marginTop:'15px'}}>
          <SearchInput />
        </div>
      </div>

      <div
        style={{
          float: 'right',
          height: '100%',
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyItems: 'center',
        }}
      >
        {username ? (
          <>
            <div style={{margin:"0 5px"}}>
              <UserButton  />
            </div>
            <div style={{margin:"0 5px"}}>
              <LogoutButton  />
            </div>
          </>
        ) : (
          <>
            <div style={{margin:"0 5px"}}>
              <LoginButton  />
            </div>
            <div>
              <RegisterButton style={{margin:"0 5px"}} />
            </div>
          </>
        )}
      </div>
    </Header>
  );
}
