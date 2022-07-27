import React, { useEffect, useState } from 'react';
import { Layout, List, Button, Space, message, Spin, Card } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import PageHeader from '../components/page_header';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { LoadingOutlined } from '@ant-design/icons';
import './watchlist.css';

const spinIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;
const { Content, Footer } = Layout;

const data_empty = [];
const data1 = [
  {
    user_name: 'test1',
    user_id: 1,
  },
  {
    user_name: 'test2',
    user_id: 2,
  },
  {
    user_name: 'test3',
    user_id: 3,
  },
];

function get_list(token) {
  axios
    .get('http://127.0.0.1:5000/mywatchlist', {
      headers: {
        'Content-Type': 'application/json',
        token: token,
      },
    })
    .then((res) => {
      return res;
    });
}

export default function Watchlist() {
  const usertoken = localStorage.getItem('token');
  const [data, setData] = useState();
  const [load, setLoad] = useState();
  const [follow, setFollow] = useState();

  const setFollowArray = (key, flag) => {
    const temp = [];
    for (const item of follow) {
      temp.push(item);
    }
    temp[key] = flag;
    setFollow(temp);
  };

  const setLoadArray = (key, flag) => {
    const temp = [];
    for (const item of load) {
      temp.push(item);
    }
    temp[key] = flag;
    setLoad(temp);
  };

  useEffect(() => {
    const tempdata = [];
    const tempfollow = [];
    const tempload = [];
    let count = 0;
    axios
      .get('http://127.0.0.1:5000/mywatchlist', {
        headers: {
          'Content-Type': 'application/json',
          token: usertoken,
        },
      })
      .then((res) => {
        console.log(res.data);
        for (const item of res.data) {
          tempdata.push({
            key: count,
            user_name: item.user_name,
            user_id: item.user_id,
          });
          count++;
          tempfollow.push(true);
          tempload.push(false);
        }
        setData(tempdata);
        setLoad(tempload);
        setFollow(tempfollow);
      });
  }, []);

  return (
    <div>
      <Layout>
        <PageHeader />
        <Content
          className='site-layout'
          style={{ padding: '0 50px', marginTop: 64 }}
        >
          <h1>My Watchlist</h1>
          <ul></ul>
          <List
            locale={{ emptyText: "You haven't followed anyone yet!" }}
            split={true}
            itemLayout='vertical'
            dataSource={data}
            renderItem={(item) => (
              <Card
                style={{
                  width: 300,
                  marginTop: 10,
                  marginBottom: 10,
                }}
              >
                <Space size={'large'}>
                  <Link
                    to={`/user?userId=${item.user_id}`}
                    className='username'
                  >
                    {item.user_name}
                  </Link>
                  {load[item.key] ? (
                    <Button
                      style={{ width: 80, paddingLeft: 0, paddingRight: 0 }}
                    >
                      <Spin indicator={spinIcon} />
                    </Button>
                  ) : follow[item.key] ? (
                    <Button
                      style={{ width: 80, paddingLeft: 0, paddingRight: 0 }}
                      type='primary'
                      onClick={() => {
                        setLoadArray(item.key, true);
                        console.log(`Unfollow ${item.user_name}`);
                        let headers = {
                          'Content-Type': 'application/json',
                          token: usertoken,
                        };
                        let data = { target_id: item.user_id };
                        axios
                          .put('http://127.0.0.1:5000/follow', data, {
                            headers,
                          })
                          .then((res) => {
                            console.log(res);
                            setFollowArray(item.key, false);
                            setLoadArray(item.key, false);
                          })
                          .catch((err) => {
                            console.log(err);
                          });
                      }}
                    >
                      Unfollow
                    </Button>
                  ) : (
                    <Button
                      style={{ width: 80, paddingLeft: 0, paddingRight: 0 }}
                      onClick={() => {
                        setLoadArray(item.key, true);
                        setFollowArray(item.key, true);
                        console.log(`Follow ${item.user_name}`);
                        let headers = {
                          'Content-Type': 'application/json',
                          token: usertoken,
                        };
                        let data = {
                          target_id: item.user_id,
                        };
                        axios
                          .post('http://127.0.0.1:5000/follow', data, {
                            headers,
                          })
                          .then((res) => {
                            console.log(res);
                            setFollowArray(item.key, true);
                            setLoadArray(item.key, false);
                          })
                          .catch((err) => {
                            console.log(err);
                          });
                        setLoadArray(item.key, false);
                      }}
                    >
                      Follow
                    </Button>
                  )}
                </Space>
              </Card>
            )}
          />
        </Content>
      </Layout>
      <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
    </div>
  );
}
