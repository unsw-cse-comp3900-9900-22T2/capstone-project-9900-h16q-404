import React, { useEffect, useState } from 'react';
import {
  Layout,
  Button,
  Input,
  Checkbox,
  DatePicker,
  Select,
  Space,
  message,
  Col,
  Row,
  InputNumber,
} from 'antd';
import PageHeader from '../components/page_header';
import axios from 'axios';
import moment from 'moment';
import './create_event.css';
import { InputComp } from './create_event';
import { useParams, useNavigate } from 'react-router-dom';

const { Content } = Layout;
const { TextArea } = Input;
const { Option } = Select;
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

  const [goldnum, setGoldnum] = useState(0);
  const [goldprice, setGoldprice] = useState();
  const [silvernum, setSilvernum] = useState(0);
  const [silverprice, setSilverprice] = useState();
  const [bronzenum, setBronzenum] = useState(0);
  const [bronzeprice, setBronzeprice] = useState();

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
      message.error('You must log in to do this!');
      back();
    }
    axios
      .get(`http://127.0.0.1:5000/event`, {
        params: {
          event_id: eventid,
        },
      })
      .then((res) => {
        console.log(res.data);
        let data = res.data.event_details[0];
        setTitle(data.event_name);
        setType(data.type);
        setStartDate(data.start_date);
        setStartTime(data.start_time);
        setEndDate(data.end_date);
        setEndTime(data.end_time);
        setLocation(data.location);
        setAdult(data.adult_only);
        setVax(data.vax_only);
        setDesc(data.description);
        setGoldnum(data.gold_num);
        setGoldprice(data.gold_price);
        setSilvernum(data.silver_num);
        setSilverprice(data.silver_price);
        setBronzenum(data.bronze_num);
        setBronzeprice(data.bronze_price);
      }, []);
  }, []);

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
    if (goldnum + silvernum + bronzenum === 0) {
      message.warning('Please define at least one valid type of tickets!');
      return false;
    }
    return true;
  };

  const confirmEdit = () => {
    if (!checkform()) {
      return;
    }
    let condition = {
      adult: adultEvent,
      vax: vaxReq,
    };
    let requestbody = {
      token: token,
      event_id: eventid,
      detail: {
        title: title,
        type: type,
        startdate: startDate,
        starttime: startTime,
        enddate: endDate,
        endtime: endTime,
        location: location,
        cond: condition,
        gold_num: goldnum,
        gold_price: goldprice,
        silver_num: silvernum,
        silver_price: silverprice,
        bronze_num: bronzenum,
        bronze_price: bronzeprice,
        desc: desc,
      },
    };
    console.log(requestbody);
    axios.put('http://127.0.0.1:5000/event', requestbody).then((res) => {
      console.log(res.data);
      let status = res.data.resultStatus;
      if (status !== 'ERROR') {
        console.log(status);
        message.success(`Successfully edit event ${title} with id ${eventid}`);
        navigate(`/event?event_id=${eventid}`);
      } else {
        message.error(`Cannot edit the event.\nMessage: ${res.data.message}`);
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

            <Space className={'InputComp'}>
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
                <Option value={'Holiday'}>Holiday</Option>
                <Option value={'Concert'}>Concert</Option>
                <Option value={'Funeral'}>Funeral</Option>
                <Option value={'Other'}>Other</Option>
              </Select>
            </Space>

            <Space>
              Start data and time
              <DatePicker
                showTime={{ format: 'HH:mm' }}
                format='YYYY-MM-DD HH:mm'
                value={moment(startDate + startTime, 'YYYY-MM-DD HH:mm')}
                placeholder={'2023-01-22 01:00'}
                onChange={(date, dateString) => {
                  let datearr = dateString.split(' ');
                  setStartDate(datearr[0]);
                  setStartTime(datearr[1]);
                }}
              />
            </Space>
            <Space>
              End data and time
              <DatePicker
                showTime={{ format: 'HH:mm' }}
                format='YYYY-MM-DD HH:mm'
                value={moment(endDate + endTime, 'YYYY-MM-DD HH:mm')}
                placeholder={'2023-01-22 01:00'}
                onChange={(date, dateString) => {
                  let datearr = dateString.split(' ');
                  console.log(datearr);
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
                You cannot edit ticket amounts and prices after you create the
                event
              </h4>

              <Row className='ticket-row' gutter={16}>
                <Col span={4}>Gold tier</Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Amount'}
                    defaultValue={0}
                    value={0 || goldnum}
                    onChange={(value) => {
                      setGoldnum(value);
                    }}
                  />
                </Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Price'}
                    addonAfter={'$'}
                    defaultValue={0}
                    value={0 || goldprice}
                    onChange={(value) => {
                      setGoldprice(value);
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
                    value={0 || silvernum}
                    onChange={(value) => {
                      setSilvernum(value);
                    }}
                  />
                </Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Price'}
                    addonAfter={'$'}
                    defaultValue={0}
                    value={0 || silverprice}
                    onChange={(value) => {
                      setSilverprice(value);
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
                    value={0 || bronzenum}
                    onChange={(value) => {
                      setBronzenum(value);
                    }}
                  />
                </Col>
                <Col span={6}>
                  <InputNumber
                    min={0}
                    addonBefore={'Price'}
                    addonAfter={'$'}
                    defaultValue={0}
                    value={0 || bronzeprice}
                    onChange={(value) => {
                      setBronzeprice(value);
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
