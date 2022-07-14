import React, { useEffect } from "react";
import { UploadOutlined } from '@ant-design/icons';
import { Form, Input, Button, Layout, DatePicker, Radio, message } from 'antd';
import PageHeader from "../components/page_header";
import { useNavigate  } from "react-router-dom";
import axios from "axios";

const { Content, Footer } = Layout;

export default function EditProfile () {

  const navigate = useNavigate();
  // check login status, if not login redirect to landing page
  useEffect(()=>{
    if (localStorage.getItem('token') === null) {
      message.error("Please login first!", 2);
      navigate("/");
    }
  }, [navigate])

  const onFinish = (values) => {
    const body = {
      "firstName": values.firstname,
      "lastName": values.lastname,
      "phone": values.phone,
      "token": localStorage.getItem('token')
    }
    axios.patch("http://127.0.0.1:5000/user/details", body)
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
  };

  const onFinishSensitive = (values) => {
    values.dateOfBirth = values.dateOfBirth.format("YYYY-MM-DD");
    values = {
      ...values,
      'vaccinated': false,
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

  return (
    <div>
      <Layout>
        <PageHeader />
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
        <h1>Edit Basic Profile</h1>
          <Form
            name="edit-basic"
            onFinish={onFinish}
          >
            <Form.Item
              label="First Name"
              name="firstname"
            >
              <Input/>
            </Form.Item>
            <Form.Item
              label="Last Name"
              name="lastname"
            >
              <Input/>
            </Form.Item>
            <Form.Item
              label="Phone"
              name="phone"
            >
              <Input/>
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            </Form.Item>
          </Form>
        <br />
        <h1>Edit Sensitive Profile</h1>
        <h4>These details relates to attendance conditions. Please edit respectfully.</h4>
          <Form
            name="edit-sensitive"
            onFinish={onFinishSensitive}
          >
            <Form.Item
              name="dateOfBirth"
              label="Date Of Birth"
            >
              <DatePicker />
            </Form.Item>

            <Form.Item
              name="gender"
              label="Gender"
            >
              <Radio.Group buttonStyle="solid">
                <Radio.Button value="Male">Male</Radio.Button>
                <Radio.Button value="Female">Female</Radio.Button>
                <Radio.Button value="LGBTQI+">LGBTQI+</Radio.Button>
                <Radio.Button value="Not Specified">Not Specified</Radio.Button>
              </Radio.Group>
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            </Form.Item>
          </Form>
        <br />
        <h1>Please upload your COVID-19 vaccination proof here</h1>
        <Button disabled icon={<UploadOutlined />}>Upload</Button>
        <br />
        
        </Content>
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
      </Layout>
    </div>
  )
}