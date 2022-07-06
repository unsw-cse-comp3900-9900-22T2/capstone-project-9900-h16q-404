import React from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import LandingPage from './pages/landing_page';
import LoginPage from './pages/login';
import RegisterPage from './pages/register';
import CreateEvent from './pages/create_event';
import EditEvent from './pages/edit_event';

function App() {
  return (
    <div>
      <Routes>
        <Route path='/' element={<LandingPage />}></Route>
        <Route path='/login' element={<LoginPage />}></Route>
        <Route path='/register' element={<RegisterPage />}></Route>
        <Route path='/create' element={<CreateEvent />}></Route>
        <Route path='/editevent/:eventid' element={<EditEvent />}></Route>
      </Routes>
    </div>
  );
}

export default App;
