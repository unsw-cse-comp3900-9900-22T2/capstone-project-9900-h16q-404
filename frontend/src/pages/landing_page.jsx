import React, { useEffect, useState } from 'react';
import { Layout, List, Avatar, Radio, message } from 'antd';
import { Link } from 'react-router-dom';
import PageHeader from '../components/page_header';
import axios from 'axios';
import RecommendationButton from '../components/recommendation_button';
import moment from 'moment'

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
            const wholeList = data.message
            let futureList = []
            const curTime = moment()
            wholeList.forEach(
              i => {
                const iFinishTime = moment(i.end_date + ' ' + i.end_time)
                if (iFinishTime.isAfter(curTime)){
                  futureList.push(i)
                }
              }
            )
            setEventList(futureList);
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
            const wholeList = data.event_details
            let futureList = []
            const curTime = moment()
            wholeList.forEach(
              i => {
                const iFinishTime = moment(i.end_date + ' ' + i.end_time)
                if (iFinishTime.isAfter(curTime)){
                  futureList.push(i)
                }
              }
            )
            setEventList(futureList);
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
            const wholeList = data
            let futureList = []
            const curTime = moment()
            wholeList.forEach(
              i => {
                const iFinishTime = moment(i.end_date + ' ' + i.end_time)
                if (iFinishTime.isAfter(curTime)){
                  futureList.push(i)
                }
              }
            )
            setEventList(futureList);
          } else {
            message.warning('No event from watched users!');
            setEventList([]);
          }
        });
    } else {
      message.warning('Filter type not available yet!');
    }
  }, [filter]);

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
          {
            localStorage.getItem('token')?
            <>
              <h1>Or you can click here to see what we recommend for you:</h1>
              <RecommendationButton />
            </>
            :
            null
          }
          <List
            itemLayout='vertical'
            size='large'
            dataSource={eventList}
            renderItem={(item) => (
              <List.Item
                key={item.id}
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
