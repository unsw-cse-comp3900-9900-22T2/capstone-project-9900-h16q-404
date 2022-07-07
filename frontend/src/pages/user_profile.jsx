import React, { useState, useEffect } from "react";
import { Layout, Avatar, Rate, Button, message } from "antd";
import PageHeader from '../components/page_header';
import "./user_profile.css"
import { UserOutlined } from '@ant-design/icons';
import { useSearchParams, Link } from "react-router-dom";

const { Content, Footer } = Layout;

export default function UserProfilePage () {

  const [searchParams] = useSearchParams();
  const [isSelfProfle, setSelfProfile] = useState(false);
  const [followed, setFollow] = useState(false);
  //const navigate = useNavigate();

  useEffect(() => {
    if(searchParams.get("self") === "true"){
      setSelfProfile(true);
      //console.log("self")
    }
    else if (searchParams.get("self") === "false") {
      setSelfProfile(false);
      //console.log("others")
      if(searchParams.get("followed") === "true"){
        console.log("followed");
        setFollow(true);
      }
      else {
        console.log("unfollowed");
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
                Nickname
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
              <h3>Age</h3>
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
                        <Button size="small" style={{marginTop:'5px'}}>Unfollow</Button>
                      </Link>
                    :
                      <Link to='/user?self=false&followed=true'>
                        <Button size="small" style={{marginTop:'5px'}}>Follow</Button>
                      </Link>  
                  )
              }
            </div>
          </div>
          <div className="rating-zone">
            <h3> Music: <Rate disabled allowHalf value={3.5}/></h3>
            <h3> Party: No enough past events</h3>
          </div>
          
        </Content>
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
      </Layout>
    </div>
  )
}