import React, { useState, useEffect } from "react"
import axios from "axios"

const LeftSideSection = () => {
  return (
    <>
      {/* transaction section */}
      <div style={{ flex: 1, backgroundColor: "pink" }}></div>
      {/* news and sentiment analysis section */}
      <NewsSection />
    </>
  )
}

const NewsSection = () => {
  // fectching from crypto panic
  const [newsData, setNewsData] = useState(null)

  async function fetchData() {
    try {
      const response = await axios.get(
        "https://cryptopanic.com//api/v1/posts/?",
        {
          params: {
            auth_token: process.env.GATSBY_NEWSAPIKEY,
            filter: "hot",
            currencies: "BTC",
          },
        }
      )
      let data = response.data.results
      console.log(data)
      setNewsData(data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [fetchData])

  // console.log(newsData)
  return <div style={{ flex: 1, backgroundColor: "orange" }}></div>
}

export default LeftSideSection
