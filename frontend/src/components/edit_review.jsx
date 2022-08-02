import React, {useState} from 'react';
import { Input, Form, Button, Rate, Comment, Avatar, message, Modal } from 'antd';
import moment from 'moment'
import axios from 'axios'
import { ExclamationCircleOutlined } from '@ant-design/icons';

const { TextArea } = Input;
const { confirm } = Modal;

const EditReviewTextArea = ({ onCommentChange, onRateChange, commentValue, rateValue, onSubmit, onClose }) => (
  <>
    <Form.Item>
      <Rate allowHalf='true' onChange={onRateChange} defaultValue={rateValue}  />
    </Form.Item>
    <Form.Item>
      <TextArea rows={4} onChange={onCommentChange} value={commentValue} />
    </Form.Item>
    <Form.Item>
      <Button htmlType="submit"  onClick={onSubmit} type="primary" style={{margin:'0 5px'}}>
        Submit
      </Button>
      <Button htmlType="submit"  onClick={onClose} style={{margin:'0 5px'}}>
        Cancel
      </Button>
    </Form.Item>
  </>
);

export default function EditReview () {
  const [visible, setVisible] = useState(false);
  const [commentValue, setCommentValue] = useState('');
  const [rateValue, setRateValue] = useState(0.0);

  const onCommentChange = (e) => {
    setCommentValue(e.target.value);
    //console.log(e)
  }

  const onRateChange = (e) => {
    setRateValue(e);
  }

  const onSubmit = () => {
    const body = {
      "token":localStorage.getItem("token"),
      "eventId":new URLSearchParams(window.location.search).get("event_id"),
      "timeStamp":moment().format("YYYY-MM-DD HH:mm"),
      "comment":commentValue,
      "rating":rateValue
    }

    axios.patch("http://127.0.0.1:5000/reviews", body)
      .then(response => response.data)
      .then(data => {
        if(data.status.toUpperCase() === "SUCCESS"){
          message.success("Updated Successfully!")
          window.location.reload();
        }
        else {
          message.error(data.message);
          return;
        }
      })
  }

  const onClose = () => {
    setVisible(false);
  }

  const onOpen = () => {
    setVisible(true);
  }

  const showDeleteReviewConfirm = () => {
    confirm({
      title: 'Are you sure delete this comment?',
      icon: <ExclamationCircleOutlined />,
      okText: 'Yes',
      okType: 'danger',
      cancelText: 'No',
  
      onOk() {
        axios.delete("http://127.0.0.1:5000/reviews",{data:{
          "token":localStorage.getItem("token"),
          "eventId":new URLSearchParams(window.location.search).get("event_id")
        }})
          .then(response => response.data)
          .then(data => {
            if(data.status.toUpperCase() === "SUCCESS"){
              message.success("Delete Successful!")
              window.location.reload()
            }
            else {
              message.error(data.message)
            }
          })
      },
  
      onCancel() {
        return;
      },
    });
  }
  
  const DeleteReviewButton = () => {
    return (
      <Button onClick={showDeleteReviewConfirm} type="danger">Delete</Button>
    )
  }

  const EditReviewButton = () => 
    (
      <Button type="primary" onClick={onOpen}>Edit</Button>
    )
  
    if(!visible){
      return (
        <div>
          <h2>You have already submitted your review.
          <br />
          You can edit or delete your review here
          </h2>
          <EditReviewButton />
          <DeleteReviewButton />
        </div>
      )
    }
    else {
      return (
        <div>
          <h2>Edit Review</h2>
          <Comment 
            avatar={<Avatar src="https://joeschmoe.io/api/v1/random" alt="Han Solo" />}
            content={
              <EditReviewTextArea 
                onCommentChange={onCommentChange}
                onRateChange={onRateChange}
                commentValue={commentValue}
                rateValue={rateValue}
                onSubmit={onSubmit}
                onClose={onClose}
              />
            }
          />
          <div>
          </div>
        </div>
      )
    }
}