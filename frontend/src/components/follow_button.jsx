import React, { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Button, Spin } from 'antd';
import axios from 'axios';
import { LoadingOutlined } from '@ant-design/icons';

/**
 * Make the Login Button a separate component
 * It can be revoked everywhere the page needs a login button
 * @returns the button component
 */

const spinIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;

export function follow_req(token, targetid) {
  axios
    .post('localhost:5000/follow', {
      headers: {
        'Content-Type': 'application/json',
        token: token,
      },
      data: { target_id: targetid },
    })
    .then((res) => {
      return res.data.resultStatus;
    });
}

export function unfollow_req(token, targetid) {
  axios
    .delete('localhost:5000/follow', {
      headers: {
        'Content-Type': 'application/json',
        token: token,
      },
      data: { target_id: targetid },
    })
    .then((res) => {
      return res.data.resultStatus;
    });
}

function get_follow (token, targetid) {
  axios
    .get('localhost:5000/follow', {
      headers: {
        'Content-Type': 'application/json',
        token: token,
      },
      params: { target_id: targetid },
    })
    .then((res) => {
      return res.data.resultStatus;
    });
}

export default function FollowButton(userId) {
  const [follow, setFollow] = useState();
  const [load, setLoad] = useState(false);
  const selfId = parseInt(localStorage.getItem('userId'));
  if (typeof userId === 'string') {
    userId = parseInt(userId);
  }

  useEffect(() => {
    console.log(typeof userId);
    console.log(userId === selfId);
    if (localStorage.getItem('userId') === undefined) {
      setFollow(false);
    } else {
      const num = Math.round(Math.random());
      console.log(num);
      if (num === 1) {
        setFollow(true);
      } else {
        setFollow(false);
      }
    }
    axios.get('http://127.0.0.1:5000/event?event_id=1').then((res) => {
      console.log(res.data.resultStatus);
    });
  }, [userId]);
  if (
    localStorage.getItem('userId') === undefined ||
    localStorage.getItem('userId') === null
  ) {
    return (
      <>
        <Button
          type='primary'
          onClick={() => {
            console.log('Please login to do this');
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
          <Button
            style={{ width: 100 }}
            href={'/watchlist'}
            onClick={() => {
              console.log('to Watchlist');
            }}
          >
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
              console.log('unfollow');
              setFollow(false);
              axios
                .get('http://127.0.0.1:5000/event?event_id=1')
                .then((res) => {
                  console.log(res);
                });
              setTimeout(() => {
                console.log('Delayed for 1 second.');
                setLoad(false);
              }, 1000);
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
              console.log('follow');
              setFollow(true);
              axios
                .get('http://127.0.0.1:5000/event?event_id=1')
                .then((res) => {
                  console.log(res);
                });
              setTimeout(() => {
                console.log('Delayed for 1 second.');
                setLoad(false);
              }, 1000);
            }}
          >
            Follow
          </Button>
        )}
      </>
    );
  }
}
