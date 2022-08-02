import React, {useState} from 'react';
import { Input, Form, Button, Rate, Comment, Avatar } from 'antd';
import moment from 'moment'

const {TextArea} = Input;
/**
 * Component for review-writing section
 * Changed from the unused /src/components/event.jsx file
 * Used on event pages
 */

const ReviewBar = ({ onCommentChange, onRateChange, commentValue, rateValue, onSubmit }) => (
  <>
    <Form.Item>
      <Rate allowHalf='true' onChange={onRateChange} defaultValue={rateValue}  />
    </Form.Item>
    <Form.Item>
      <TextArea rows={4} onChange={onCommentChange} value={commentValue} />
    </Form.Item>
    <Form.Item>
      <Button htmlType="submit"  onClick={onSubmit} type="primary">
        Add Review
      </Button>
    </Form.Item>
  </>
);

export default function WriteReview (props) {
  const [rateValue, setRateValue] = useState(0.0);
  const [commentValue, setCommentValue] = useState('');

  const onCommentChange = (e) => {
    setCommentValue(e.target.value);
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

    props.handleSubmit(body);
  }

  return (
    <div>
      <h2>Please Leave your Review: </h2>
      <Comment
        avatar={<Avatar src="https://joeschmoe.io/api/v1/random" alt="Han Solo" />}
        content={
          <ReviewBar
            onCommentChange={onCommentChange}
            onRateChange={onRateChange}
            commentValue={commentValue}
            rateValue={rateValue}
            onSubmit={onSubmit}
          />
        }
      >

      </Comment>
    </div>
  )
};