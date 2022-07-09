import React, { useState, useEffect } from "react";
import { Layout, Avatar, Rate, Button, message, List } from "antd";
import PageHeader from '../components/page_header';
import "./user_profile.css"
import { UserOutlined } from '@ant-design/icons';
import { useSearchParams, Link } from "react-router-dom";

const { Content, Footer } = Layout;

const followButtonOnClick = () => {
  console.log("Trying to follow...");
}

const unfollowButtonOnClick = () => {
  console.log("Trying to unfollow...");
}

export default function UserProfilePage () {

  const [searchParams] = useSearchParams();
  const [isSelfProfle, setSelfProfile] = useState(false);
  const [followed, setFollow] = useState(false);
  //const navigate = useNavigate();

  useEffect(() => {

    // THESE PARTS TO BE CHANGED! 

    if(searchParams.get("self") === "true"){
      setSelfProfile(true);
      //console.log("self")
    }
    else if (searchParams.get("self") === "false") {
      setSelfProfile(false);
      //console.log("others")
      if(searchParams.get("followed") === "true"){
        //console.log("followed");
        setFollow(true);
      }
      else {
        //console.log("unfollowed");
        setFollow(false);
      }
    }
    else{
      message.error("Oops... Something went wrong")
    }
    //console.log(searchParams.get("self"))
  },[searchParams])

  // WARNING
  // All "self=" related searchParames MUST be changed to userID after backend is completed
  // /user?userId=xxxx

  return (
    <div>
      <Layout>
        <PageHeader />
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
          <div className="basic-profile-zone">
            <div className="name-zone">
              <h1>
                Anonymous User
                { 
                  isSelfProfle ? 
                    <Link to='/edit_profile'>
                      <Button>Edit Profile</Button>
                    </Link>
                  : 
                    <></>}
              </h1>
              <h3>email</h3>
              <h3>dob</h3>
              <h3>Gender</h3>
              <h3>Phone</h3>
              <h3>COVID-19 Vaccination Proof</h3>
            </div>
            <div className="picture-zone">
              <Avatar size={128} icon={<UserOutlined />} style={{marginTop:'20px'}}/>
              {
                isSelfProfle? 
                  <Button type="primary" size="small" style={{marginTop:'5px'}}>Watchlist</Button>
                : 
                  (
                    followed? 
                      <Link to='/user?self=false&followed=false'>
                        <Button size="small" style={{marginTop:'5px'}} onClick={unfollowButtonOnClick}>Unfollow</Button>
                      </Link>
                    :
                      <Link to='/user?self=false&followed=true'>
                        <Button size="small" style={{marginTop:'5px'}} onClick={followButtonOnClick}>Follow</Button>
                      </Link>  
                  )
              }
            </div>
          </div>
          <div className="rating-zone">
            <h3> Music: <Rate disabled allowHalf value={3.5}/></h3>
            <h3> Party: No enough past events</h3>
          </div>
          
          <div className="event-zone">
            <List
              size="small"
              header={<div>Past Events</div>}
              bordered
              dataSource={["mock past event 1", "mock past event 2"]}
              renderItem={(item) => <List.Item>{item}</List.Item>}
              >
            </List>
            <br />
            <List
              size="small"
              header={<div>Upcoming Events</div>}
              bordered
              dataSource={["mock upcoming event 1", "mock upcoming event 2"]}
              renderItem={(item) => <List.Item>{item}</List.Item>}
            >
            </List>
          </div>
        </Content>
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
      </Layout>
    </div>
  )
}