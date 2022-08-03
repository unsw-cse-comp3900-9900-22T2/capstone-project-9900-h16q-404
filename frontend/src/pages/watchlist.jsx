import React, { useEffect, useState } from 'react';
import { Layout, List, Button, Space, message, Spin, Card, Avatar } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import PageHeader from '../components/page_header';
import axios from 'axios';
import { LoadingOutlined } from '@ant-design/icons';
import './watchlist.css';

const spinIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;
const { Content, Footer } = Layout;

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
        for (const item of res.data) {
          tempdata.push({
            key: count,
            user_name: item.user_name,
            user_id: item.user_id,
            image: item.image,
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
          <List
            grid={{
              gutter: 16,
              xs: 1,
              sm: 2,
              md: 2,
              lg: 3,
              xl: 4,
              xxl: 4,
            }}
            locale={{ emptyText: "You haven't followed anyone yet!" }}
            split={true}
            itemLayout='vertical'
            dataSource={data}
            renderItem={(item) => (
              <List.Item
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                }}
              >
                <Card
                  style={{
                    marginTop: 10,
                    marginBottom: 10,
                    borderColor: 'grey',
                  }}
                  hoverable={true}
                  size={'small'}
                >
                  <div
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                    }}
                  >
                    {item.image === 'default' || item.image === null ? (
                      <Avatar
                        size={64}
                        icon={<UserOutlined />}
                        style={{ marginTop: '20px' }}
                      />
                    ) : (
                      <Avatar size={64} src={item.image} />
                    )}
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
                              message.success('Successfully unfollow the user');
                              setFollowArray(item.key, false);
                              setLoadArray(item.key, false);
                            })
                            .catch((err) => {
                              message.error(err.data);
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
                              message.success(res.data);
                              setFollowArray(item.key, true);
                              setLoadArray(item.key, false);
                            })
                            .catch((err) => {
                              message.error(err.data);
                            });
                          setLoadArray(item.key, false);
                        }}
                      >
                        Follow
                      </Button>
                    )}
                  </div>
                </Card>
              </List.Item>
            )}
          />
        </Content>
      </Layout>
      <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
    </div>
  );
}
