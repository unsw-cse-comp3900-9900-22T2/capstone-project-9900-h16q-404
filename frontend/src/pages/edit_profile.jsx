import React, { useEffect, useState } from 'react';
import { Button, Layout, message, Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import PageHeader from '../components/page_header';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { uploadImg } from '../components/image';

import { InputComp } from '../components/InputComp';

const { Content, Footer } = Layout;

export default function EditProfile() {
  const navigate = useNavigate();
  // use hooks to set all attributes
  const [firstname, setFirstname] = useState('');
  const [lastname, setLastname] = useState('');
  const [phone, setPhone] = useState('');
  const [image, setImage] = useState('');

  // check login status, if not login redirect to landing page
  useEffect(() => {
    if (localStorage.getItem('token') === null) {
      message.error('Please login first!', 2);
      navigate('/');
    }
    // add a GET request to fetch user profile old details
    const requestURL =
      'http://127.0.0.1:5000/user?userId=' + localStorage.getItem('userId');
    axios
      .get(requestURL)
      .then((res) => res.data.message)
      .then((data) => {
        setFirstname(data.firstname);
        setLastname(data.lastname);
        setPhone(data.phone);
        setImage(data.image);
      });
  }, [navigate]);

  const onFinish = () => {
    const body = {
      firstName: firstname,
      lastName: lastname,
      phone: phone,
      image: image,
      token: localStorage.getItem('token'),
    };
    axios
      .patch('http://127.0.0.1:5000/user/details', body)
      .then((res) => res.data)
      .then((data) => {
        const resultStatus = data.resultStatus;
        const info = data.message;
        if (resultStatus === 'SUCCESS') {
          message.success(info);
          localStorage.setItem('userIcon', image);
          const detailsLocation =
            '/user?userId=' + localStorage.getItem('userId');
          navigate(detailsLocation);
        } else {
          message.error(info);
        }
      });
  };

  const onBack = () => {
    navigate(-1);
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
            <h1 style={{ marginTop: '5px', marginBottom: '5px' }}>
              Edit Profile
            </h1>
            <br></br>
            <InputComp
              addon='First name'
              defValue={''}
              value={firstname || ''}
              placeholder={''}
              setter={setFirstname}
            />
            <InputComp
              addon={'Last name'}
              defValue={''}
              value={lastname || ''}
              placeholder={''}
              setter={setLastname}
            />
            <InputComp
              addon={'Phone'}
              defValue={''}
              value={phone || ''}
              placeholder={''}
              setter={setPhone}
            />
            <div className='picture-zone'>
              {image === 'default' || image === null ? (
                <Avatar
                  size={128}
                  icon={<UserOutlined />}
                  style={{ marginTop: '20px' }}
                />
              ) : (
                <Avatar size={128} src={image} style={{ marginTop: '20px' }} />
              )}
              {uploadImg(
                setImage,
                '(Optional) Upload an icon for your profile:'
              )}
              <Button
                style={{ margin: 4 }}
                onClick={() => {
                  setImage('default');
                }}
              >
                Use the default icon
              </Button>
            </div>
          </div>
          <div>
            Want to change email or password?{' '}
            <a href='/edit_login_credential'>
              Click here to edit login credentials.
            </a>
            <br />
            Want to change admittance related details?{' '}
            <a href='/edit_sensitive_profile'>
              Click here to edit sensitive details.
            </a>
          </div>
          <br />
          <div className='ButtonSet'>
            <Button onClick={onFinish} className='Sendbutton' type='primary'>
              Send
            </Button>
            <Button onClick={onBack} className='Sendbutton'>
              Back
            </Button>
          </div>
          <br />
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </div>
  );
}
