import React, { useEffect, useState } from 'react';
import {
  Layout,
  Button,
  Input,
  Checkbox,
  DatePicker,
  TimePicker,
  Space,
  message,
  Col,
  Row,
  InputNumber,
} from 'antd';
import PageHeader from '../components/page_header';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import moment from 'moment';
import {} from 'antd';

import './create_event.css';
import PropTypes from 'prop-types';

const { Content } = Layout;
const { TextArea } = Input;

function fileToDataURL(setImage, file) {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function () {
    setImage(reader.result);
    console.log(reader.result);
  };
  reader.onerror = function (error) {
    alert(`Invalid image type. Please try again. Error: ${error}`);
  };
}

export const uploadImg = (setImage) => {
  return (
    <>
      (Optional) Upload an image for your event:
      <div id='upload-question-img' className='input-group'>
        <Input
          type='file'
          onChange={(e) => {
            const [file] = e.target.files;
            fileToDataURL(setImage, file);
          }}
        />
      </div>
    </>
  );
};

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

  const [ticket, setTicket] = useState({
    gold: { number: 0, price: 0 },
    silver: { number: 0, price: 0 },
    bronze: { number: 0, price: 0 },
  });

  const dateFormat = 'YYYY-MM-DD';
  const timeFormat = 'HH:mm';

  const [adultEvent, setAdult] = useState(false);
  const [vaxReq, setVax] = useState(false);

  const navigate = useNavigate();
  const test = () => {
    setTitle('testtitle');
    setType('Concert');
    setStartDate('2020-01-01');
    setStartTime('01:01');
    setEndDate('2020-01-02');
    setEndTime('02:02');
    setLocation('here');
    setAdult(true);
    setDesc('testdesc');
  };
  useEffect(() => {
    if (localStorage.getItem('username')) {
      setToken(localStorage.getItem('username'));
    } else {
      message.error('You must log in to do this!');
      back();
    }
    test();
  }, [setToken]);

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

    if (desc === '' || desc === undefined) {
      message.warning('Please input event description');
      return false;
    }
    return true;
  };

  const back = () => {
    navigate(-1);
  };

  const checkboxChange = (e, setter) => {
    setter(e.target.checked);
  };

  const create = () => {
    if (!checkform()) {
      return;
    }
    let condition = {
      adult: adultEvent,
      vax: vaxReq,
    };
    let requestbody = {
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
        gold_num: ticket.gold.num,
        gold_price: ticket.gold.price,
        silver_num: ticket.silver.num,
        silver_price: ticket.silver.price,
        bronze_num: ticket.bronze.num,
        bronze_price: ticket.bronze.price,
        desc: desc,
      },
    };
    console.log(requestbody);
    axios.post('http://127.0.0.1:5000/create', requestbody).then((res) => {
      console.log(res.data);
      let status = res.data.status;
      let id = res.data.new_event_id[0];
      if (status !== 'Error') {
        console.log(id);
        message.success(`Successfully create event ${title} with id ${id}`);
        navigate(`/event?event_id=${id}`);
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
            <Space>
              Start data and time
              <DatePicker
                className={'InputComp'}
                showTime={{ format: 'HH:mm' }}
                format='YYYY-MM-DD HH:mm'
                placeholder={'2023-01-22 01:00'}
                onChange={(date, dateString) => {
                  let datearr = dateString.split(' ');
                  setStartDate(datearr[0]);
                  setStartTime(datearr[1]);
                }}
              />
            </Space>
            <Space>
              End date and time
              <DatePicker
                className={'InputComp'}
                showTime={{ format: 'HH:mm' }}
                format='YYYY-MM-DD HH:mm'
                placeholder={'2023-01-25 01:00'}
                onChange={(date, dateString) => {
                  let datearr = dateString.split(' ');
                  setEndDate(datearr[0]);
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
            <div className='ticket-sect'>
              <h3>Ticket Infomation</h3>
              <h4>You can write details of ticket tiers in description</h4>
              <h4>Caution: After creating the event you will not be able to edit the infomation of tickets!</h4>
              <Row className='ticket-row' gutter={16}>
                <Col span={4}>Gold tier</Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Amount'}
                    defaultValue={0}
                    onChange={(value) => {
                      ticket.gold.number = value;
                    }}
                  />
                </Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Price'}
                    addonAfter={'$'}
                    defaultValue={0}
                    onChange={(value) => {
                      ticket.gold.price = value;
                    }}
                  />
                </Col>
              </Row>
              <Row className='ticket-row' gutter={16}>
                <Col span={4}>Silver tier</Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Amount'}
                    defaultValue={0}
                    onChange={(value) => {
                      ticket.silver.number = value;
                    }}
                  />
                </Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Price'}
                    addonAfter={'$'}
                    defaultValue={0}
                    onChange={(value) => {
                      ticket.silver.price = value;
                    }}
                  />
                </Col>
              </Row>
              <Row className='ticket-row' gutter={16}>
                <Col span={4}>Bronze tier</Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Amount'}
                    defaultValue={0}
                    onChange={(value) => {
                      ticket.bronze.number = value;
                    }}
                  />
                </Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Price'}
                    addonAfter={'$'}
                    defaultValue={0}
                    onChange={(value) => {
                      ticket.bronze.price = value;
                    }}
                  />
                </Col>
              </Row>
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
            <img src={image} />
            {uploadImg(setImage)}

            <div className='ButtonSet'>
              <Space>
                <Button onClick={create} type='primary' className='Sendbutton'>
                  Send
                </Button>
                <Button onClick={back} className='Sendbutton'>
                  Back
                </Button>
              </Space>
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
