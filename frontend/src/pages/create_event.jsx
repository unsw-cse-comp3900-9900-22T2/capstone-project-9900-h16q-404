import React, { useEffect, useState, } from 'react';
import {
  Layout,
  Button,
  Input,
  Checkbox,
  DatePicker,
  Space,
  message,
  Col,
  Row,
  InputNumber,
  Select,
} from 'antd';
import PageHeader from '../components/page_header';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import moment from 'moment';
import { uploadImg } from '../components/image';

import './create_event.css';
import { InputComp } from '../components/InputComp';

const { Content, Footer } = Layout;
const { TextArea } = Input;
const { Option } = Select;

/*
Event name
Event type
  “Other”
  “Festival”
  “Party”
  “Music”
  “Sport”
  “Film”
  “Food & Drink”
  “Business”
  “Funeral”
Attendance Conditions
Start Time
End time
Location
Tickets
Description
Pictures
*/

export default function CreateEvent() {
  const [token, setToken] = useState();
  const [title, setTitle] = useState();
  const [type, setType] = useState('Other');
  const gutter = 16;
  const span = 6;

  const [startDate, setStartDate] = useState();
  const [startTime, setStartTime] = useState();
  const [endDate, setEndDate] = useState();
  const [endTime, setEndTime] = useState();
  const [location, setLocation] = useState();
  const [desc, setDesc] = useState();
  const [image, setImage] = useState('default');

  const [ticket, setTicket] = useState({
    gold: { number: 0, price: 0 },
    silver: { number: 0, price: 0 },
    bronze: { number: 0, price: 0 },
  });

  const [adultEvent, setAdult] = useState(false);
  const [vaxReq, setVax] = useState(false);

  const navigate = useNavigate();

  const ticketRow_ = (classString, type) => {
    // reserved for later use
    return (
      <Row className='ticket-row' gutter={gutter} style={{ marginTop: 6 }}>
        <Col span={2}>{classString}</Col>
        <Col span={span}>
          <Input addonBefore={'Name'} />
        </Col>
        <Col span={span}>
          <InputNumber
            min={0}
            addonBefore={'Amount'}
            defaultValue={0}
            onChange={(value) => {
              type.number = value;
            }}
          />
        </Col>
        <Col span={span}>
          <InputNumber
            min={0}
            addonBefore={'Price'}
            addonAfter={'$'}
            defaultValue={0}
            onChange={(value) => {
              type.price = value;
            }}
          />
        </Col>
      </Row>
    );
  };

  const ticketRow = (classString, type) => {
    return (
      <Row className='ticket-row' gutter={gutter} style={{ marginTop: 6 }}>
        <Col span={4}>{classString}</Col>
        <Col span={span}>
          <InputNumber
            min={0}
            addonBefore={'Amount'}
            defaultValue={0}
            onChange={(value) => {
              type.number = value;
            }}
          />
        </Col>
        <Col span={span}>
          <InputNumber
            min={0}
            addonBefore={'Price'}
            addonAfter={'$'}
            defaultValue={0}
            onChange={(value) => {
              type.price = value;
            }}
          />
        </Col>
      </Row>
    );
  };

  useEffect(() => {
    if (localStorage.getItem('token')) {
      setToken(localStorage.getItem('token'));
    } else {
      // Yunran: no username means not logged in, should redirect to landing page
      message.error('You have not logged in!', 2);
      navigate('/');
    }
  }, [setToken, navigate]);

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

    if (moment(startDate + startTime, 'YYYY-MM-DDHH:mm') <= moment()) {
      message.warning('Please select a start time later than now!');
      return false;
    }

    if (
      moment(startDate + startTime, 'YYYY-MM-DDHH:mm') >=
      moment(endDate + endTime, 'YYYY-MM-DDHH:mm')
    ) {
      message.warning('The end time should be later than start time');
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
    if (
      ticket.gold.number + ticket.silver.number + ticket.bronze.number ===
      0
    ) {
      message.warning('Please define at least one valid type of tickets!');
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
    let headers = {
      token: token,
    };
    let requestbody = {
      detail: {
        title: title,
        type: type,
        startdate: startDate,
        starttime: startTime,
        enddate: endDate,
        endtime: endTime,
        location: location,
        cond: condition,
        gold_num: ticket.gold.number,
        gold_price: ticket.gold.price,
        silver_num: ticket.silver.number,
        silver_price: ticket.silver.price,
        bronze_num: ticket.bronze.number,
        bronze_price: ticket.bronze.price,
        desc: desc,
        image: image,
      },
    };
    console.log(requestbody);
    axios
      .post('http://127.0.0.1:5000/create', requestbody, { headers })
      .then((res) => {
        console.log(res.data);
        let status = res.data.status;
        let id = res.data.new_event_id[0];
        if (status !== 'ERROR') {
          console.log(id);
          message.success(`Successfully create event ${title} with id ${id}`);
          navigate(`/event?event_id=${id}`);
        } else {
          message.error(
            `There is something wrong when creating the event.\nMessage: ${res.data.message}`
          );
        }
      });
  };

  return (
    <div>
      <Layout>
        <PageHeader />
        <Content
          className='site-layout'
          style={{ padding: '0 50px', marginTop: 64 }}
        >
          <div className='new_event'>
            <h1>Create event</h1>
            <InputComp
              addon={'Title'}
              defValue={''}
              value={title || ''}
              placeholder={'UNSW Show'}
              setter={setTitle}
            />

            <Space className={'InputComp'} style={{ minWidth: 90 }}>
              Type:
              <Select
                value={'' || type}
                defaultValue={'Other'}
                onChange={(value) => {
                  setType(value);
                }}
                style={{ minWidth: 140, maxWidth: 200 }}
              >
                <Option value={'Business'}>Business</Option>
                <Option value={'Party'}>Party</Option>
                <Option value={'Music'}>Music</Option>
                <Option value={'Sport'}>Sport</Option>
                <Option value={'Food & Drink'}>Food & Drink</Option>
                <Option value={'Film'}>Film</Option>
                <Option value={'Festival'}>Festival</Option>
                <Option value={'Funeral'}>Funeral</Option>
                <Option value={'Holiday'}>Holiday</Option>
                <Option value={'Other'}>Other</Option>
              </Select>
            </Space>

            <Space>
              Start date and time
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
              <h4>
                Caution: After creating the event you will not be able to edit
                the infomation of tickets!
              </h4>
              {ticketRow('Gold Tier', ticket.gold)}
              {ticketRow('Silver Tier', ticket.silver)}
              {ticketRow('Bronze Tier', ticket.bronze)}
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

            <div>
              {uploadImg(
                setImage,
                '(Optional) Upload an image for your event:'
              )}
              {image !== null && image !== 'default' ? (
                <div>
                  <img src={image} style={{ maxWidth: 800, maxHeight: 600 }} />
                </div>
              ) : (
                <></>
              )}
              <Button
                style={{ margin: 4 }}
                onClick={() => {
                  setImage('default');
                }}
              >
                Clear
              </Button>
            </div>

            <div className='ButtonSet' style={{ marginBottom: 6 }}>
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
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
      </Layout>
    </div>
  );
}
