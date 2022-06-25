import React from "react";
import { Layout } from 'antd';
import logo from '../static/picacg.jpeg'
import LoginButton from '../components/login_button';
import RegisterButton from '../components/register_button';
import SearchInput from "./search_input";

const { Header } = Layout;

export default function PageHeader () {
  return (
    <Header style={{
      position: 'fixed',
      zIndex: 1,
      width: '100%'
    }}>
      <div style={{
        float: 'left', 
        height:'100%', 
        display:'flex', 
        flexDirection: 'row', 
        alignItems:'center', 
        justifyItems:'center',
        textAlign:'center'
      }}>
        <img src={logo} alt="Logo" style={{width: '45px', height: '45px', marginRight:'5px'}}/>
        <h1 style={{color:'white', fontSize:"bold", marginRight:'15px'}}>LiveKnight</h1>
        <SearchInput/>
      </div>

      <div style={{
        float: 'right',
        height: '100%',
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyItems: 'center'
      }}>
        <LoginButton />
        <RegisterButton />
      </div>
    </Header>
  )
}