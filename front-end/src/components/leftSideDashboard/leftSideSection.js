import React, { useState, useEffect } from "react"
import axios from "axios"
import * as Icon from "react-cryptocoins"
import moment from "moment"
import TransactionSection from "./TransactionSection"

//  Main view
const LeftSideSection = () => {
  return (
    <>
      {/* transaction section */}
      <TransactionSection />
      {/* news and sentiment analysis section */}
      <NewsSection />
    </>
  )
}

//  mock news data
const newsData = [
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Positive",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "10h",
  },
  {
    title:
      "ETH Hits $3852, Raoul Pal Says Investors He Knows 'Shifting Allocation to ETH Over BTCâ€™",
    sentiment: "Positive",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13h",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Positive",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "22h",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Negative",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13/05, 20:17",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Positive",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13/05, 20:17",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Negative",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13/05, 20:17",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Negative",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13/05, 20:17",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Negative",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13/05, 20:17",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Negative",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13/05, 20:17",
  },
  {
    title: "Top Three Weekend Gainers: ARRR, MATIC, and TEL",
    sentiment: "Negative",
    link:
      "https://beincrypto.com/top-three-weekend-gainers-arrr-matic-and-tel/",
    date: "13/05, 20:17",
  },
]

const NewsSection = () => {
  // fectching from crypto panic
  // const [newsData, setNewsData] = useState(null)

  // async function fetchData() {
  //   try {
  //     const response = await axios.get(
  //       "https://cryptopanic.com//api/v1/posts/?",
  //       {
  //         params: {
  //           auth_token: process.env.GATSBY_NEWSAPIKEY,
  //           filter: "hot",
  //           currencies: "BTC",
  //         },
  //       }
  //     )
  //     let data = response.data.results
  //     console.log(data)
  //     setNewsData(data)
  //   } catch (error) {
  //     console.error(error)
  //   }
  // }

  // useEffect(() => {
  //   fetchData()
  // }, [fetchData])

  // console.log(newsData)
  return (
    <div style={{ flex: 1 }}>
      <div
        style={{
          backgroundColor: "rgba(232,236,239,0.2)",
          width: "100%",
          height: 2,
        }}
      ></div>
      <p
        style={{
          marginRight: "60%",
          color: "white",
          marginTop: "2%",
          marginLeft: "5%",
          marginBottom: "1%",
        }}
      >
        Top News
      </p>
      {newsData.slice(0, 8).map(article => {
        return (
          <>
            <SingleNewsContainer data={article} />
            <div
              style={{
                backgroundColor: "rgba(232,236,239,0.2)",
                width: "100%",
                height: 2,
              }}
            ></div>
          </>
        )
      })}
    </div>
  )
}

// function to extract host name from url
function extractDomain(url) {
  var domain
  //find & remove protocol (http, ftp, etc.) and get domain
  if (url.indexOf("://") > -1) {
    domain = url.split("/")[2]
  } else {
    domain = url.split("/")[0]
  }

  //find & remove www
  if (domain.indexOf("www.") > -1) {
    domain = domain.split("www.")[1]
  }

  domain = domain.split(":")[0] //find & remove port number
  domain = domain.split("?")[0] //find & remove url params

  return domain
}

const SingleNewsContainer = ({ data }) => {
  const link = extractDomain(data.link) // returns host name ie cryptonews.com

  return (
    <div
      style={{
        // backgroundColor: "pink",
        width: "100%",
        fontSize: 12,
        color: "white",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-evenly",
        padding: 10,
      }}
    >
      <div style={{ color: "rgb(152, 169, 188)", fontSize: 12, flex: 2 }}>
        {data.date}
      </div>
      <div style={{ fontSize: 12, width: "40%", flex: 4 }}>{data.title}</div>
      <div style={{ color: "rgb(152, 169, 188)", fontSize: 12, flex: 2 }}>
        {link}
      </div>
      <div
        style={{
          flex: 1,
          alignItems: "center",
          display: "flex",
          justifyContent: "center",
          border:
            data.sentiment === "Positive"
              ? "1.3px solid #60BC3F"
              : "1.3px solid #DB3E62",
          padding: 5,
          borderRadius: 5,
          color: data.sentiment === "Positive" ? "#60BC3F" : "#DB3E62",
        }}
      >
        {data.sentiment}
      </div>
    </div>
  )
}

export default LeftSideSection
