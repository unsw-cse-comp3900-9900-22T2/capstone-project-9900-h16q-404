import React, { useEffect, useState } from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined } from '@ant-design/icons';
import { Layout, List, Space, Avatar, Radio, message } from 'antd';
import { Link } from 'react-router-dom';
import PageHeader from '../components/page_header';
import axios from 'axios';

const { Content, Footer } = Layout;

export default function LandingPage() {
  // hook
  const [eventList, setEventList] = useState();
  const [filter, setFilter] = useState('All');

  const onFilterButtonChange = (e) => {
    setFilter(e.target.value);
    return;
  };

  const FilterButtonGroup = () => {
    // check login status
    if (localStorage.getItem('token')) {
      return (
        <Radio.Group
          size='large'
          defaultValue={filter}
          buttonStyle='solid'
          onChange={onFilterButtonChange}
        >
          <Radio.Button value='All'>All</Radio.Button>
          <Radio.Button value='Festival'>Festival</Radio.Button>
          <Radio.Button value='Party'>Party</Radio.Button>
          <Radio.Button value='Music'>Music</Radio.Button>
          <Radio.Button value='Sport'>Sport</Radio.Button>
          <Radio.Button value='Film'>Film</Radio.Button>
          <Radio.Button value='Food and Drink'>Food & Drink</Radio.Button>
          <Radio.Button value='Business'>Business</Radio.Button>
          <Radio.Button value='Funeral'>Funeral</Radio.Button>
          <Radio.Button value='Others'>Others</Radio.Button>
          <Radio.Button value='Follower'>Events from My Watchlist</Radio.Button>
        </Radio.Group>
      );
    } else {
      return (
        <Radio.Group
          size='large'
          defaultValue={filter}
          buttonStyle='solid'
          onChange={onFilterButtonChange}
        >
          <Radio.Button value='All'>All</Radio.Button>
          <Radio.Button value='Festival'>Festival</Radio.Button>
          <Radio.Button value='Party'>Party</Radio.Button>
          <Radio.Button value='Music'>Music</Radio.Button>
          <Radio.Button value='Sport'>Sport</Radio.Button>
          <Radio.Button value='Film'>Film</Radio.Button>
          <Radio.Button value='Food and Drink'>Food & Drink</Radio.Button>
          <Radio.Button value='Business'>Business</Radio.Button>
          <Radio.Button value='Funeral'>Funeral</Radio.Button>
          <Radio.Button value='Others'>Others</Radio.Button>
        </Radio.Group>
      );
    }
  };

  useEffect(() => {
    if (filter === 'All') {
      axios
        .get('http://127.0.0.1:5000/events', {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        .then((response) => response.data)
        .then((data) => {
          if (data.resultStatus === 'SUCCESS') {
            setEventList(data.message);
          }
        });
    } else if (
      filter !== 'Others' &&
      filter !== 'All' &&
      filter !== 'Follower'
    ) {
      const filterURL =
        'http://127.0.0.1:5000/filter?filterType=' + encodeURIComponent(filter);
      axios
        .get(filterURL)
        .then((response) => response.data)
        .then((data) => {
          if (data.resultStatus === 'SUCCESS') {
            setEventList(data.event_details);
          } else {
            message.warning(data.message);
            setEventList([]);
          }
        });
    } else if (filter === 'Follower') {
      const filterURL = 'http://127.0.0.1:5000/watchedevents';
      axios
        .get(filterURL, {
          headers: {
            'Content-Type': 'application/json',
            token: localStorage.getItem('token'),
          },
        })
        .then((response) => response.data)
        .then((data) => {
          if (data.length !==0) {
            setEventList(data);
          } else {
            message.warning('No event from watched users!');
            setEventList([]);
          }
        });
    } else {
      message.warning('Filter type not available yet!');
    }
  }, [filter]);

  const IconText = ({ icon, text }) => (
    <Space>
      {React.createElement(icon)}
      {text}
    </Space>
  );

  return (
    <div>
      <Layout>
        <PageHeader />
        <Content
          className='site-layout'
          style={{ padding: '0 50px', marginTop: 64 }}
        >
          <div className='filter-area' style={{ marginTop: '5px' }}>
            <div
              style={{
                fontSize: '300%',
                fontWeight: 'bold',
                fontFamily: 'Arial, Helvetica, sans-serif',
              }}
            >
              Ready for your next event ride?
            </div>
          </div>
          <h1>Please select to filter the type of events you want to see: </h1>
          <FilterButtonGroup />
          <List
            itemLayout='vertical'
            size='large'
            dataSource={eventList}
            renderItem={(item) => (
              <List.Item
                key={item.id}
                actions={[
                  <IconText
                    icon={StarOutlined}
                    text='114'
                    key='list-vertical-star-o'
                  />,
                  <IconText
                    icon={LikeOutlined}
                    text='514'
                    key='list-vertical-like-o'
                  />,
                  <IconText
                    icon={MessageOutlined}
                    text='1919'
                    key='list-vertical-message'
                  />,
                ]}
                extra={
                  <img
                    width={272}
                    alt='logo'
                    src='https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png'
                  />
                }
              >
                <List.Item.Meta
                  avatar={
                    <Avatar src={'https://joeschmoe.io/api/v1/random'}></Avatar>
                  }
                  title={
                    <Link to={'/event?event_id=' + item.id}>
                      {item.event_name}
                    </Link>
                  }
                  description={
                    <Link to={'/user?userId=' + item.host}>
                      {item.host_username}
                    </Link>
                  }
                />
                {'Event date: ' + item.start_date}
              </List.Item>
            )}
          ></List>
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </div>
  );
}
