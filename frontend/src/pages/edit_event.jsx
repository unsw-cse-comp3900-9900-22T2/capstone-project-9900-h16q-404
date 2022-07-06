import React, { useEffect, useState } from 'react';
import { Layout, Button } from 'antd';
import PageHeader from '../components/page_header';
import axios from 'axios';
import { Input } from 'antd';
import './create_event.css';
import { InputComp } from './create_event';
import { useParams, useNavigate } from 'react-router-dom';

const { Content } = Layout;
const { TextArea } = Input;
/*
Event name
Event type
Attendance Conditions
Start Time
End time
Location
Description
Pictures (optional - if we have time and its easy)
No tickets yet
*/

// /editevent/eventid
export default function EditEvent() {
  const params = useParams();
  const eventid = params.eventid;
  const gameId = params.gameId;
  const [token, setToken] = useState('');
  const [title, setTitle] = useState('');
  const [type, setType] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [location, setLocation] = useState('');
  const [desc, setDesc] = useState('');
  const [image, setImage] = useState('');
  const [cond, setCond] = useState();

  useEffect(() => {
    if (localStorage.getItem('username')) {
      setToken(localStorage.getItem('username'));
    } else {
      setToken('None');
    }
    test();
  }, [setToken, setDesc]);

  const test = () => {
    setDesc('test');
  };

  const confirmEdit = () => {
    let new_event = JSON.stringify({
      id: eventid,
      token: token,
      title: title,
      type: type,
      starttime: startTime,
      endtime: endTime,
      location: location,
      desc: desc,
    });
    console.log(new_event);
  };

  return (
    <>
      <Layout>
        <PageHeader />
        <Content
          className='create_content'
          style={{ padding: '0 50px', marginTop: 64 }}
        >
          <div className='new_event'>
            <InputComp
              addon={'Title'}
              defValue={''}
              value={title || ''}
              placeholder={'UNSW Show'}
              setter={setTitle}
            />
            <InputComp
              addon={'Type'}
              defValue={''}
              value={type || ''}
              placeholder={'Show'}
              setter={setType}
            />
            <InputComp
              addon={'Start Time'}
              defValue={''}
              value={startTime || ''}
              placeholder={'2023-01-22'}
              setter={setStartTime}
            />
            <InputComp
              addon={'End Time'}
              defValue={''}
              value={endTime || ''}
              placeholder={'2023-01-25'}
              setter={setEndTime}
            />
            <InputComp
              addon={'Location'}
              defValue={''}
              value={location || ''}
              placeholder={'High st 5 Kensington, NSW 2033'}
              setter={setLocation}
            />
            <h3>Description</h3>
            <TextArea
              rows={3}
              placeholder='Please type the description'
              showCount='true'
              value={desc || ''}
              onChange={(e) => {
                setDesc(e.target.value);
              }}
            />
            <div className='ButtonSet'>
              <Button onClick={confirmEdit} type='primary'>
                Send
              </Button>
              <Button>Cancel</Button>
            </div>
          </div>
        </Content>
      </Layout>
    </>
  );
}
