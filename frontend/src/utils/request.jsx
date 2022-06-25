import { message } from 'antd';
// import getToken from './getToken';

// const API_PORT = require('../config.json');
const API_HOST = 'http://127.0.0.1:5000';

// function to distinguish if request needs a body
// not important in first demo
/*
function needBody (url, method = 'GET') {
  method = method.toUpperCase();
  if (url === '/admin/auth/logout') {
    return false;
  } else if (url.startsWith('/admin/quiz/') && url !== ('/admin/quiz/new') && method === 'POST') {
    return false;
  } else if (method === 'GET' || method === 'DELETE') {
    return false;
  } else {
    return true;
  }
}
*/

// function to distinguish if request needs autorization
// not important in first demo
/*
function needAuthorization (url) {
  if (url.startsWith('/play/')) {
    return false;
  } else if (url === '/admin/auth/register' || url === '/admin/auth/login') {
    return false;
  } else {
    return true;
  }
}
*/


export default function request (url, method = 'GET', body = undefined) {
  const feed = {
    method: method.toUpperCase(),
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      // Authorization: (needAuthorization(url) ? `Bearer ${getToken()}` : undefined),
      Authorization: undefined,
    },
    cache: 'no-cache',
    body,
  }

  return fetch(`${API_HOST}${url}`, feed)
    .then(res => res.json())
    .then(data => {
      // not used before login function works
      /*
      if (data.error) {
        if (data.error.includes('Invalid Token')) {
          message.error('Your session has expired! Please login again!');
          // clean localstorage and refresh page
          localStorage.clear();
          window.location.href = '/';
        } else {
          message.error(data.error, 'error');
        }
        return;
      }
      */
      console.log('Data from backend: ' + JSON.stringify(data));
      return data;
    });
}
