import React, { useState, useEffect } from 'react';
import { Layout, Avatar, Rate, Button, message, List } from 'antd';
import PageHeader from '../components/page_header';
import './user_profile.css';
import { UserOutlined } from '@ant-design/icons';
import { useSearchParams, Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const { Content, Footer } = Layout;

export default function UserProfilePage() {
  const [searchParams] = useSearchParams();
  const [isSelfProfle, setSelfProfile] = useState(false);
  const [followed, setFollow] = useState(false);
  const [details, setDetails] = useState({});
  const navigate = useNavigate();

  const followButtonOnClick = () => {
    console.log('Trying to follow...');
    setFollow(true);
  };

  const unfollowButtonOnClick = () => {
    console.log('Trying to unfollow...');
    setFollow(false);
  };

  useEffect(() => {
    // compare the userId in params with userId in localStorage
    if (searchParams.get('userId') === localStorage.getItem('userId')) {
      setSelfProfile(true);
    } else if (searchParams.get('userId') !== localStorage.getItem('userId')) {
      setSelfProfile(false);
      setFollow(false);
      // get rid of followed or not in this stage
      /*
      if(searchParams.get("followed") === "true"){
        //console.log("followed");
        setFollow(true);
      }
      else {
        //console.log("unfollowed");
        setFollow(false);
      }
      */
    } else {
      message.error('Oops... Something went wrong');
    }

    const requestURL =
      'http://127.0.0.1:5000/user?userId=' + searchParams.get('userId');
    axios
      .get(requestURL, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((res) => res.data.message)
      .then((data) => {
        //console.log(data);
        setDetails(data);
      });
  }, [searchParams]);

  let fullname = '';
  if (details.firstname === null && details.lastname === null) {
    fullname = 'Anonymous user';
  } else {
    fullname = details.firstname + ' ' + details.lastname;
  }

  return (
    <div>
      <Layout>
        <PageHeader />
        <Content
          className='site-layout'
          style={{ padding: '0 50px', marginTop: 64 }}
        >
          <div className='basic-profile-zone'>
            <div className='name-zone'>
              <h1>
                {'Welcome, ' + fullname}
                {isSelfProfle ? (
                  <Link to='/edit_profile'>
                    <Button>Edit Profile</Button>
                  </Link>
                ) : (
                  <></>
                )}
              </h1>
              <h3>Email: {details.email}</h3>
              <h3>
                Date of birth:{' '}
                {details.dateOfBirth === null ? 'Unknown' : details.dateOfBirth}
              </h3>
              <h3>
                Gender:{' '}
                {details.gender === null ? 'Not Specified' : details.gender}
              </h3>
              <h3>
                Phone: {details.phone === null ? 'Unknown' : details.phone}{' '}
              </h3>
              <h3>
                COVID-19 Vaccination Proof:{' '}
                {details.vac === true ? 'Verified' : 'Not verified'}
              </h3>
            </div>
            <div className='picture-zone'>
              <Avatar
                size={128}
                icon={<UserOutlined />}
                style={{ marginTop: '20px' }}
              />
              {isSelfProfle ? (
                <Button
                  type='primary'
                  size='small'
                  style={{ marginTop: '5px' }}
                >
                  Watchlist
                </Button>
              ) : followed ? (
                <Button
                  size='small'
                  style={{ marginTop: '5px' }}
                  onClick={unfollowButtonOnClick}
                >
                  Unfollow
                </Button>
              ) : (
                <Button
                  size='small'
                  style={{ marginTop: '5px' }}
                  onClick={followButtonOnClick}
                >
                  Follow
                </Button>
              )}
            </div>
          </div>
          <div className='rating-zone'>
            <h3>
              {' '}
              Music: <Rate disabled allowHalf value={3.5} />
            </h3>
            <h3> Party: No enough past events</h3>
          </div>

          <div className='event-zone'>
            <Button
              type='primary'
              onClick={() => {
                navigate('/create');
              }}
            >
              Create event
            </Button>
            <List
              size='small'
              header={<div>Past Events</div>}
              bordered
              dataSource={['mock past event 1', 'mock past event 2']}
              renderItem={(item) => <List.Item>{item}</List.Item>}
            ></List>
            <br />
            <List
              size='small'
              header={<div>Upcoming Events</div>}
              bordered
              dataSource={['mock upcoming event 1', 'mock upcoming event 2']}
              renderItem={(item) => <List.Item>{item}</List.Item>}
            ></List>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </div>
  );
}
