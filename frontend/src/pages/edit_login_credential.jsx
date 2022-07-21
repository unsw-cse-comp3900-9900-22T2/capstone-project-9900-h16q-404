import React, { useEffect } from 'react';
import { Form, Input, Button, Layout, message } from 'antd'
import PageHeader from '../components/page_header';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const { Content, Footer } = Layout;

/**
 * Logic Recommended for back-end: 
 * Email and oldPassword needed to change email
 * oldPassword and newPassword needed to change password
 * all fields needed to change both email and password
 * if oldPassword not correct, prevent all changes and return 403 Forbidden from back-end.
 */

const EditLoginCredentialForm = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  // check login status, if not login redirect to landing page
  useEffect(()=>{
    if (localStorage.getItem('token') === null) {
      message.error("Please login first!", 2);
      navigate("/");
    }
  }, [navigate])

  const onFinishLoginCredential = (values) => {
    const body = {
      "old_password": values.oldPassword,
      "new_password": values.newPassword,
      "token": localStorage.getItem("token")
    }
    axios.patch("http://127.0.0.1:5000/user/login_credentials", body)
      .then(res => res.data)
      .then(data => {
        const resultStatus= data.resultStatus;
        const info = data.message;
        if (resultStatus === "SUCCESS"){
          //if successful, logout the current user!
          message.success(info);
          localStorage.clear();
          navigate("/");
        }
        else {
          message.error(info);
        }
      })
  }

  return (
    <Form
      name="edit-login"
      form={form}
      onFinish={onFinishLoginCredential}
    >
      <Form.Item
        label="Old Password"
        name="oldPassword"
      >
        <Input.Password />
      </Form.Item>
      <Form.Item
        label="New Password"
        name="newPassword"
        dependencies={['oldPassword']}
        hasFeedback
        rules={[
          ({ getFieldValue }) => ({
            validator(_, value) {
            if (!value || getFieldValue('oldPassword') !== value) {
              return Promise.resolve();
            }
      
            return Promise.reject(new Error('New password can not be same as old password!'));
            },
          }),
        ]}
      >
        <Input.Password />
      </Form.Item>
      <Form.Item
        label="Confirm New Password"
        name="confirm"
        dependencies={['newPassword']}
        hasFeedback
        rules={[
          ({ getFieldValue }) => ({
            validator(_, value) {
            if (!value || getFieldValue('newPassword') === value) {
              return Promise.resolve();
            }
      
            return Promise.reject(new Error('The two passwords that you entered do not match!'));
            },
          }),
        ]}
      >
        <Input.Password/>
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  )
}

export default function EditLoginCredential () {
  
  return (
    <>
      <Layout>
        <PageHeader />
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
          <h1>Edit Login Credentials</h1>
          <EditLoginCredentialForm />
        </Content>
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
      </Layout>
    </>
  )
}