import React, { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Button } from 'antd';
import axios from 'axios';

/**
 * Make the Login Button a separate component
 * It can be revoked everywhere the page needs a login button
 * @returns the button component
 */

export default function FollowButton(userId) {
  const [follow, setFollow] = useState();
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
      console.log(res);
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
            onClick={() => {
              console.log('to Watchlist');
            }}
          >
            Watchlist
          </Button>
        ) : follow ? (
          <Button
            onClick={() => {
              console.log('unfollow');
              setFollow(false);
              axios
                .get('http://127.0.0.1:5000/event?event_id=1')
                .then((res) => {
                  console.log(res);
                });
            }}
          >
            Unfollow
          </Button>
        ) : (
          <Button
            type='primary'
            onClick={() => {
              console.log('follow');
              setFollow(true);
              axios
                .get('http://127.0.0.1:5000/event?event_id=1')
                .then((res) => {
                  console.log(res);
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
