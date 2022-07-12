import React, { useEffect, useState } from 'react';
import {
  Layout,
  Button,
  Input,
  Checkbox,
  DatePicker,
  TimePicker,
  Space,
  message
} from 'antd';
import PageHeader from '../components/page_header';
import axios from 'axios';
import moment from 'moment';
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

  const [token, setToken] = useState();
  const [title, setTitle] = useState();
  const [type, setType] = useState();
  const [startDate, setStartDate] = useState();
  const [startTime, setStartTime] = useState();
  const [endDate, setEndDate] = useState();
  const [endTime, setEndTime] = useState();

  const [location, setLocation] = useState();
  const [desc, setDesc] = useState();
  const [image, setImage] = useState();

  const dateFormat = 'YYYY-MM-DD';
  const timeFormat = 'HH:mm';

  const [adultEvent, setAdult] = useState(false);
  const [vaxReq, setVax] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem('username')) {
      setToken(localStorage.getItem('username'));
    } else {
      setToken('None');
    }
    axios
      .get(`https://localhost:5000/event`, {
        params: {
          eventid: eventid,
        },
      })
      .then((res) => {
        console.log(res.data);
        let data = res.data.detail;
        setTitle(data.title);
        setType(data.type);
        setStartDate(data.startdate);
        setStartTime(data.starttime);
        setEndDate(data.enddate);
        setEndTime(data.enddate);
        setLocation(data.location);
        setAdult(true);
        setVax(true);
        setDesc(data.desc);
      }, []);
  }, []);

  const test = () => {
    setDesc('test');
    setTitle('test');
    setStartDate('2020-01-01');
    setStartTime('01:01');
    setEndDate('2021-01-01');
    setEndTime('02:02');
    setAdult(true);
    setVax(true);
  };

  const checkform = () => {
    if (title === '' || title === undefined) {
      message.warning('Please input event title');
      return false;
    }

    if (type === '' || type === undefined) {
      message.warning('Please select event type');
      return false;
    }

    if (startDate === '' || startDate === undefined) {
      message.warning('Please select start time of the event');
      return false;
    }

    if (endDate === '' || endDate === undefined) {
      message.warning('Please select end time of the event');
      return false;
    }

    if (location === '' || location === undefined) {
      message.warning('Please input event location');
      return false;
    }

    console.log(desc);
    if (desc === "" || desc === undefined) {
      message.warning('Please input event description');
      return false;
    }
    return true;
  };

  const confirmEdit = () => {
    if (!checkform()) {
      return;
    }
    console.log(title);
    let condition = {
      adult: adultEvent,
      vax: vaxReq,
    };
    let requestbody = JSON.stringify({
      token: token,
      id: eventid,
      detail: {
        title: title,
        type: type,
        startdate: startDate,
        starttime: startTime,
        enddate: endDate,
        endtime: endTime,
        location: location,
        cond: condition,
        desc: desc,
      },
    });
    console.log(requestbody);
    console.log('update');
    axios
      .put(
        'https://48c72885-2eec-4a6a-aa5c-c752ef2afe8e.mock.pstmn.io/updateevent',
        requestbody
      )
      .then((res) => {
        console.log(res.data);
        let status = res.data.status;
        if (status !== 'Error') {
          console.log('success');
        }
      });
  };

  const back = () => {
    navigate(-1);
  };

  const checkboxChange = (e, setter) => {
    setter(e.target.checked);
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
            <Space>
              Start data and time
              <DatePicker
                showTime={{ format: 'HH:mm' }}
                format='YYYY-MM-DD HH:mm'
                value={moment(startDate + startTime, 'YYYY-MM-DD HH:mm')}
                placeholder={'2023-01-22 01:00'}
                onChange={(date, dateString) => {
                  let datearr = dateString.split(' ');
                  setStartDate(dateString);
                  setStartTime(datearr[1]);
                }}
              />
            </Space>
            <Space>
              Start data and time
              <DatePicker
                showTime={{ format: 'HH:mm' }}
                format='YYYY-MM-DD HH:mm'
                value={moment(endDate + endTime, 'YYYY-MM-DD HH:mm')}
                placeholder={'2023-01-22 01:00'}
                onChange={(date, dateString) => {
                  let datearr = dateString.split(' ');
                  setEndDate(dateString);
                  setEndTime(datearr[1]);
                }}
              />
            </Space>
            <InputComp
              addon={'Location'}
              defValue={''}
              value={location || ''}
              placeholder={'High st 5 Kensington, NSW 2033'}
              setter={setLocation}
            />
            <div className='conditionSect'>
              <h3>Additonal Conditions</h3>
              <p>
                <Checkbox
                  checked={adultEvent}
                  onChange={(event) => checkboxChange(event, setAdult)}
                >
                  This is an adult-only event.
                </Checkbox>
              </p>
              <p>
                <Checkbox
                  checked={vaxReq}
                  onChange={(event) => checkboxChange(event, setVax)}
                >
                  Customers must be fully vaccinated.
                </Checkbox>
              </p>
            </div>
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
              <Button
                onClick={confirmEdit}
                type='primary'
                className='Sendbutton'
              >
                Send
              </Button>
              <Button onClick={back} className='Sendbutton'>
                Back
              </Button>
            </div>
          </div>
        </Content>
      </Layout>
    </>
  );
}
