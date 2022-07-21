import React from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import LandingPage from './pages/landing_page';
import LoginPage from './pages/login';
import RegisterPage from './pages/register';
import UserProfilePage from './pages/user_profile';
import EditProfile from './pages/edit_profile';
import EditLoginCredential from './pages/edit_login_credential';
import SearchResult from './pages/search_result';
import EventPage from './pages/event_page';
import CreateEvent from './pages/create_event';
import EditEvent from './pages/edit_event';
import MyTicket from './pages/my_ticket';
import EditSensitiveProfile from './pages/edit_sensitive_profile';
import BuyTicket from './pages/buyticket';

function App () {
  return (
    <div>
      <Routes>
        <Route path='/' element={<LandingPage />}></Route>
        <Route path='/login' element={<LoginPage />}></Route>
        <Route path='/register' element={<RegisterPage />}></Route>
        <Route path='/user' element={<UserProfilePage />}></Route>
        <Route path='/edit_profile' element={<EditProfile />}></Route>
        <Route path='/edit_login_credential' element={<EditLoginCredential />}></Route>
        <Route path='/search' element={<SearchResult />}></Route>
        <Route path='/event' element={<EventPage />}></Route>
        <Route path='/create' element={<CreateEvent />}></Route>
        <Route path='/editevent/:eventid' element={<EditEvent />}></Route>
        <Route path='/my_ticket' element={<MyTicket />}></Route>
        <Route path='/edit_sensitive_profile' element={<EditSensitiveProfile />}></Route>
        <Route path='/buyticket/:eventid' element={<BuyTicket />}></Route>
      </Routes >
    </div >
  );
}

export default App;
