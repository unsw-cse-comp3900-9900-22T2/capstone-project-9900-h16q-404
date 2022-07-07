import React, { useEffect, useState } from 'react';
import { Layout, Button } from 'antd';
import PageHeader from '../components/page_header';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import moment from 'moment';
import { Input, Checkbox, DatePicker, TimePicker } from 'antd';

import './create_event.css';
import PropTypes from 'prop-types';

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
export default function CreateEvent() {
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
  const timeFormat = 'HH:mm:ss';

  const [adultEvent, setAdult] = useState(false);
  const [vaxReq, setVax] = useState(false);

  const navigate = useNavigate();

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

  const back = () => {
    navigate(-1);
  };

  const checkboxChange = (e, setter) => {
    setter(e.target.checked);
  };

  const create = () => {
    let condition = {
      adult: adultEvent,
      vax: vaxReq,
    };
    let requestbody = JSON.stringify({
      token: token,
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
    axios
      .post(
        'https://48c72885-2eec-4a6a-aa5c-c752ef2afe8e.mock.pstmn.io/createevent',
        requestbody
      )
      .then((res) => {
        console.log(res.data);
        let status = res.data.status;
        let id = res.data.id;
        if (status !== 'Error') {
          console.log(id);
        }
      });
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
            <div>
              Start data and time
              <DatePicker
                placeholder={'2023-01-22'}
                onChange={(date, dateString) => {
                  setStartDate(dateString);
                }}
              />
              <TimePicker
                onChange={(time, timeString) => {
                  setStartTime(timeString);
                }}
              />
            </div>
            <div>
              End date and time
              <DatePicker
                placeholder={'2023-01-25'}
                onChange={(date, dateString) => {
                  setEndDate(dateString);
                }}
              />
              <TimePicker
                onChange={(time, timeString) => {
                  setEndTime(timeString);
                }}
              />
            </div>
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
              <Button onClick={create} type='primary' className='Sendbutton'>
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

export const InputComp = ({ addon, defValue, value, placeholder, setter }) => {
  return (
    <>
      <Input
        className={'InputComp'}
        addonBefore={addon}
        defaultValue={defValue}
        value={value}
        placeholder={placeholder}
        onChange={(e) => {
          setter(e.target.value);
        }}
      />
    </>
  );
};

InputComp.protTypes = {
  addon: PropTypes.string,
  defValue: PropTypes.string,
  value: PropTypes.string,
  placeholder: PropTypes.string,
  setter: PropTypes.func,
};
