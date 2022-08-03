import React, { useEffect, useState } from 'react';
import { Button, message, Spin } from 'antd';
import axios from 'axios';
import { LoadingOutlined } from '@ant-design/icons';

/**
 * Make the Login Button a separate component
 * It can be revoked everywhere the page needs a login button
 * @returns the button component
 */

const spinIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;

export default function FollowButton(userId) {
  const [follow, setFollow] = useState();
  const [load, setLoad] = useState(false);
  const selfId = parseInt(localStorage.getItem('userId'));
  const token = localStorage.getItem('token');
  if (typeof userId === 'string') {
    userId = parseInt(userId);
  }

  useEffect(() => {
    if (
      localStorage.getItem('token') === undefined ||
      localStorage.getItem('token') === null
    ) {
      setFollow(false);
    } else {
      axios
        .get('http://127.0.0.1:5000/follow', {
          headers: {
            'Content-Type': 'application/json',
            token: token,
          },
          params: { target_id: userId },
        })
        .then((res) => {
          setFollow(res.data);
        })
        .catch((err) => {
          message.error(err.data);
        });
    }
  }, [token]);
  if (
    localStorage.getItem('userId') === undefined ||
    localStorage.getItem('userId') === null
  ) {
    return (
      <>
        <Button
          type='primary'
          onClick={() => {
            message.error('Please login to do this');
          }}
        >
          Follow
        </Button>
      </>
    );
  } else {
    return (
      <>
        {selfId === userId ? (
          <Button style={{ width: 100 }} href={'/watchlist'}>
            Watchlist
          </Button>
        ) : load ? (
          <Button style={{ width: 100 }}>
            <Spin indicator={spinIcon} />
          </Button>
        ) : follow ? (
          <Button
            style={{ width: 100 }}
            onClick={() => {
              setLoad(true);
              let headers = {
                'Content-Type': 'application/json',
                token: token,
              };
              let data = { target_id: userId };
              axios
                .put('http://127.0.0.1:5000/follow', data, { headers })
                .then((res) => {
                  message.success('Successfully unfollow the user');
                  setFollow(false);
                  setLoad(false);
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
            style={{ width: 100 }}
            type='primary'
            onClick={() => {
              setLoad(true);
              let headers = {
                'Content-Type': 'application/json',
                token: token,
              };
              let data = { target_id: userId };
              axios
                .post('http://127.0.0.1:5000/follow', data, { headers })
                .then((res) => {
                  message.success(res.data);
                  setFollow(true);
                  setLoad(false);
                })
                .catch((err) => {
                  message.error(err.data);
                });
            }}
          >
            Follow
          </Button>
        )}
      </>
    );
  }
}
