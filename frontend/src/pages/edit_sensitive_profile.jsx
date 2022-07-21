import React, { useEffect, useState } from "react";
import { UploadOutlined, CheckOutlined } from '@ant-design/icons';
import { Button, Layout, DatePicker, Radio, message, Space } from 'antd';
import PageHeader from "../components/page_header";
import moment from 'moment';
import { useNavigate  } from "react-router-dom";
import axios from "axios";

// borrow some input fields from create event
import './create_event.css';

const { Content, Footer } = Layout;

export default function EditSensitiveProfile () {
  const navigate = useNavigate();

  // use hooks to store all detailse
  const [dob, setDOB] = useState("");
  const [gender, setGender] = useState("Not Specified");
  const [vaccinated, setVax] = useState(false);

  const PreUploadButton = () => {
    if (! vaccinated) {
      return (
        <Button 
          icon={<UploadOutlined />}
          onClick={() => {
            message.success("Uploded Successfully")
            setVax(true);
          }}
        >
          Upload</Button>
      )
    }
    else {
      return (
        <Button icon={<CheckOutlined />} disabled>Uploaded!</Button>
      )
    }
  }

  const FlexCalendar = () => {
    if(!dob){
      return (
        <DatePicker 
          format='YYYY-MM-DD'
          onChange={(date, dateString) => {
            setDOB(dateString);
          }}
        />
      )
    }
    else {
      return (
        <DatePicker 
          format='YYYY-MM-DD'
          value={moment(dob || "","YYYY-MM-DD")}
          onChange={(date, dateString) => {
            setDOB(dateString);
          }}
        />
      )
    }
  }

  const FlexGenderPicker = () => {
    if(!gender){
      return(
        <Radio.Group 
          buttonStyle="solid"
          onChange={onGenderChange}
        >
          <Radio.Button value="Male">Male</Radio.Button>
          <Radio.Button value="Female">Female</Radio.Button>
          <Radio.Button value="LGBTQI+">LGBTQI+</Radio.Button>
          <Radio.Button value="Not Specified">Not specified</Radio.Button>
        </Radio.Group>
      )
    }
    else{
      return(
        <Radio.Group 
          buttonStyle="solid"
          onChange={onGenderChange}
          defaultValue={gender}
        >
          <Radio.Button value="Male">Male</Radio.Button>
          <Radio.Button value="Female">Female</Radio.Button>
          <Radio.Button value="LGBTQI+">LGBTQI+</Radio.Button>
          <Radio.Button value="Not Specified">Not specified</Radio.Button>
        </Radio.Group>
      )
    }
  }

  const onFinishSensitive = () => {
    const values = {
      'vaccinated': vaccinated,
      'gender': gender,
      'dateOfBirth': dob,
      'token': localStorage.getItem('token')
    }
    axios.patch('http://127.0.0.1:5000/user/sensitive_details', values)
      .then(res => res.data)
      .then(data => {
        const resultStatus= data.resultStatus;
        const info = data.message;
        if (resultStatus === "SUCCESS") {
          message.success(info);
          const detailsLocation = '/user?userId='+localStorage.getItem('userId');
          navigate(detailsLocation);
        }
        else{
          message.error(info);
        }
      })
  }

  const onBack = () => {
    navigate(-1);
  }

  const onGenderChange = ({ target: { value } }) => {
    setGender(value);
  }

  useEffect( () => {
    if (localStorage.getItem('token') === null) {
      message.error("Please login first!", 2);
      navigate("/");
    }
    const requestURL =
    'http://127.0.0.1:5000/user?userId=' + localStorage.getItem("userId");
    axios.get(requestURL)
      .then((res) => res.data.message)
      .then((data)=>{
        setGender(data.gender);
        setVax(data.vac);
        setDOB(data.dateOfBirth);
      })

  },[navigate])

  return (
    <>
      <Layout>
        <PageHeader />
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
          <div className="new_event">
            <h1>Edit Sensitive Profile</h1>
            <br />
            <h4>These details relates to attendance conditions. Please edit respectfully.</h4>
            <Space>
              Date of birth
              <FlexCalendar />
            </Space>
            <br />
            <Space>
              Gender
              <FlexGenderPicker />
            </Space>
            <br />
            <Space>
              Please upload your COVID-19 vaccination proof at here <PreUploadButton />
            </Space>
            <Space>
              Want to change email or password? <a href='/edit_login_credential'>Click here to edit login credentials.</a>
            </Space>
            <Space>
            Want to change normal details? <a href="/edit_profile">Click here to edit general profile.</a> 
            </Space>
          </div>
          <div className="ButtonSet">
            <Button
              onClick={onFinishSensitive}
              className='Sendbutton'
              type="primary"
            >Send</Button>
            <Button
              onClick={onBack}
              className='Sendbutton'
            >Back</Button>
          </div>
        </Content>
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
      </Layout>
    </>
  )
}