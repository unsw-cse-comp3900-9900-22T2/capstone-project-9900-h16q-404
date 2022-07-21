import React, { useEffect } from "react";
import { Layout } from "antd";
import PageHeader from "../components/page_header";
import { useSearchParams } from "react-router-dom";

const { Content, Footer } = Layout;

export default function SearchResult () {
  const [searchParams] = useSearchParams();

  useEffect(()=>{
    const value = decodeURIComponent(searchParams.get("keyword"));
    const keyWordList = value.split(" ");
    const keyWordDict = {
      keyWordList: keyWordList.map(word => {
        return word.toLowerCase();
      })
    }
    console.log(JSON.stringify(keyWordDict));
  }, [searchParams])
  return (
    <>
      <Layout>
        <PageHeader />
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
          <h1>Results of searching {decodeURIComponent(searchParams.get("keyword"))}: </h1>
        </Content>
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
      </Layout>
    </>
  )
}