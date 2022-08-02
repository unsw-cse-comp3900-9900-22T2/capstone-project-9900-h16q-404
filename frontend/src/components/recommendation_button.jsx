import React, {useState} from "react";
import { Button } from 'antd';


export default function RecommendationButton () {
  const [loadings, setLoadings] = useState(false)

  function mockGetData() {
    console.log("data request sent")
    setLoadings(true)
    setTimeout(() => {
      console.log("data response seen!")
      setLoadings(false)
    }, 5000)
  }

  const handleClick = () => {
    mockGetData()
  }

  return (
    <Button
      type="primary"
      loading={loadings}
      onClick={handleClick}
      size='large'
    >
      Recommended for me
    </Button>
  )
}