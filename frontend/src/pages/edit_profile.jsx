import React, { useEffect } from "react";
import { UploadOutlined } from '@ant-design/icons';
import { Form, Input, Button, Layout, DatePicker, Radio, message } from 'antd';
import PageHeader from "../components/page_header";
import { useNavigate  } from "react-router-dom";

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
    console.log(values);
  };

  const onFinishSensitive = (values) => {
    values.dateOfBirth = values.dateOfBirth.format("YYYY-MM-DD");
    console.log(values);
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
        <h4>Warning: you can only change the following profile once a month</h4>
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
                <Radio.Button value="male">Male</Radio.Button>
                <Radio.Button value="female">Female</Radio.Button>
                <Radio.Button value="lgbtqi+">LGBTQI+</Radio.Button>
                <Radio.Button value="not-specified">Not Specified</Radio.Button>
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