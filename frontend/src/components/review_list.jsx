import React, { useState } from "react";
import { Comment, List, Tooltip, Rate, Input, Form, Button, Modal, Avatar, Divider, message } from 'antd';
import moment from 'moment';
import { ExclamationCircleOutlined } from '@ant-design/icons';
import WriteReview from "./write_review";
import EditReview from "./edit_review";
import axios from 'axios';
import { useEffect } from "react";

const { TextArea } = Input;
const { confirm } = Modal;

/**
 * Host Reply Related functions
 */

// The text area for event host replying to existing reviews [start]
const ReplyTextArea = ({onChange, onSubmit, onClose, value}) => 
  (
    <>
      <Form.Item>
        <TextArea 
          rows={4} onChange={onChange} value={value}
        />
      </Form.Item>
      <Form.Item>
        <Button size="small" type="primary" onClick={onSubmit} style={{margin:"0 5px"}}>Reply</Button>
        <Button size="small" onClick={onClose} style={{margin:"0 5px"}}>Cancel</Button>
      </Form.Item>
    </>
  )
// The text area for event host replying to existing reviews [end]

// The "reply" button for event host replying existing reviews and relating functions [start]
const ReplyButton = (props) => {
  const [commentArea, setCommentArea] = useState(false);
  const [value, setValue] = useState('');

  const openCommentArea = () => {
    setCommentArea(true);
  }
  
  const closeCommentArea = () => {
    setCommentArea(false);
  }

  const sendComment = () => {
    const body = {
      "token":localStorage.getItem('token'),
      "eventId":parseInt(new URLSearchParams(window.location.search).get("event_id")),
      "targetUserId":props.targetUserId,
      "timeStamp":moment().format("YYYY-MM-DD HH:mm"),
      "reply": value
    }

    axios.patch("http://127.0.0.1:5000/hostreplies", body)
      .then(response => response.data)
      .then(data => {
        if (data.status.toUpperCase() === "SUCCESS") {
          window.location.reload()
        }
        else {
          message.error(data.message);
        }
      })
  }

  const onContentChange = (e) => {
    setValue(e.target.value);
  }

  return (
    <>
      {commentArea?
        <>
        <Comment avatar={<Avatar src="https://joeschmoe.io/api/v1/random" alt="Han Solo" />}
          content={
            <ReplyTextArea
              onChange={onContentChange}
              onSubmit={sendComment}
              onClose={closeCommentArea}
              value={value}
            />
          }
        />
        </>
      :
        <>
          <span key="comment-list-reply-to-0" onClick={openCommentArea}>Reply to</span>
        </>
      }
    </>
  )
}
// The "reply" button for event host replying existing reviews and relating functions [end]

/**
 * Host deleting reply functions
 */

// The confirm prompt of deleting reply on reviews [start]
const showDeleteConfirm = (targetUserId) => {
  confirm({
    title: 'Are you sure delete this reply?',
    icon: <ExclamationCircleOutlined />,
    okText: 'Yes',
    okType: 'danger',
    cancelText: 'No',

    onOk() {
      axios.delete("http://127.0.0.1:5000/hostreplies", {data:{
        "token":localStorage.getItem("token"),
        "eventId":new URLSearchParams(window.location.search).get("event_id"),
        "targetUserId":targetUserId
      }})
        .then(response => response.data)
        .then(data => {
          if (data.status.toUpperCase() === "SUCCESS") {
            window.location.reload();
          }
          else {
            message.error(data.message);
          }
        })
    },

    onCancel() {
      return;
    },
  });
};
// The confirm prompt of deleting reply on reviews [end]

// Then "delete button" for event host deleting their replies on reviews [start]
const DeleteReplyButton = ({targetUserId}) => {
  const deleteAction = () => {
    showDeleteConfirm(targetUserId)
  }
  return (
    <span key="comment-list-reply-to-0" onClick={deleteAction}>Delete Reply</span>
  )
}
// Then "delete button" for event host deleting their replies on reviews [end]

// component export

export default function ReviewList (props) {

  const [reviewList, setReviewList] = useState({});

  const handleReviewSubmit = (e) => {
    axios.post("http://127.0.0.1:5000/reviews", e)
      .then(res=>res.data)
      .then(data=>{
        if (data.status.toUpperCase() === "SUCCESS"){
          message.success("Review Posted!")
          window.location.reload();
        }
        else {
          message.error(data.message);
          return;
        }
      })
  }

  useEffect(()=>{
    const requestURL = "http://127.0.0.1:5000/reviews?token="
      +localStorage.getItem("token")
      +"&eventId="+props.eventId;
    axios.get(requestURL)
      .then(response => response.data.message)
      .then(data => {
        setReviewList(data)
      })
  },[props])

  const WriteReviewSection = () => {
    if (!reviewList.has_ticket){
      return(
        <h2>Sorry you can't post a review on this event, since you have not attended it.</h2>
      )
    }
    else {
      if(reviewList.has_comment){
        return(
          <EditReview />
        )
      }
      else {
        return(
          <WriteReview handleSubmit={handleReviewSubmit} />
        )
      }
    }
  }

  return (
    <>
    <Divider orientation="left">Write Review</Divider>
    <WriteReviewSection handleSubmit={handleReviewSubmit} />
    <Divider orientation="left">Review List</Divider>
    <List
      className="comment-list"
      itemLayout="horizontal"
      dataSource={reviewList.reviews}
      renderItem={(item) => (
        <li>
          <Comment
            actions={reviewList.is_host? (item.reply? null : [<ReplyButton targetUserId={item.reviewedByUserId} />]) : null}
            author={item.reviewedBy}
            avatar='https://joeschmoe.io/api/v1/random'
            content={
              <div>
                <Rate disabled allowHalf defaultValue={item.rating}/>
                <br />
                {item.review}
              </div>
            }
            datetime={
              <Tooltip title={moment(item.reviewedOn).format('YYYY-MM-DD HH:mm:ss')}>
                <span>{moment(item.reviewedOn).fromNow()}</span>
              </Tooltip>
            }
          >
            {
              item.reply ? 
              <Comment 
                actions={props.isEventHost? [<DeleteReplyButton targetUserId={item.reviewedByUserId} />] : null}
                author={reviewList.hostedBy}
                avatar='https://joeschmoe.io/api/v1/random'
                content={item.reply}
                datetime={
                  <Tooltip title={moment(item.repliedOn).format('YYYY-MM-DD HH:mm')}>
                    <span>{moment(item.repliedOn).fromNow()}</span>
                  </Tooltip>
                }
              ></Comment>
              :
              null
            }
          </Comment>
        </li>
      )}
  />
  </>
  )
}