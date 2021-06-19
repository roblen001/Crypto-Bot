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

const NewsSection = () => {
  const [newsFilter, setNewsFilter] = useState("top")
  const [topNews, setTopNews] = useState([])
  const [allNews, setAllNews] = useState([])
  const [newsData, setNewsData] = useState([])

  async function fetchTopNews() {
    try {
      const response = await axios.get(
        // limit this to 10 so it can fit in container
        "http://192.168.2.117:5000/news/top/8"
      )
      // TODO: THIS IS A TEMP FIX
      let data = response.data
      console.log("top")
      console.log(data)
      data.replace("[", "")
      data.replace("]", "")
      console.log(JSON.parse(data))
      setTopNews(data)
      setNewsData(data)
    } catch (error) {
      console.error(error)
    }
  }

  async function fetchAllNews() {
    try {
      const response = await axios.get(
        // limit this to 10 so it can fit in container
        "http://192.168.2.117:5000/news/all/8"
      )

      let data = response.data
      console.log(typeof data)
      setAllNews(data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchTopNews()
    fetchAllNews()
  }, [])

  return (
    <div style={{ flex: 1 }}>
      <div
        style={{
          backgroundColor: "rgba(232,236,239,0.2)",
          width: "100%",
          height: 2,
        }}
      ></div>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
        }}
      >
        <p
          style={{
            marginRight: "5%",
            color: "white",
            marginTop: "2%",
            marginLeft: "5%",
            marginBottom: "1%",
          }}
        >
          News
        </p>
        <button
          style={{
            backgroundColor: "transparent",
            color: "white",
            fontSize: 12,
            height: "1%",
            borderRadius: 12,
            borderWidth: 1,
            borderColor: newsFilter == "top" ? "white" : "transparent",
            marginTop: "2%",
            alignSelf: "center",
          }}
          onClick={() => {
            setNewsFilter("top")
            setNewsData(topNews)
          }}
        >
          Top
        </button>
        <button
          style={{
            backgroundColor: "transparent",
            color: "white",
            fontSize: 12,
            height: "1%",
            borderRadius: 12,
            borderWidth: 1,
            borderColor: newsFilter == "latest" ? "white" : "transparent",
            marginTop: "2%",
            alignSelf: "center",
            marginLeft: "2%",
          }}
          onClick={() => {
            setNewsFilter("latest")
            setNewsData(allNews)
          }}
        >
          Latest
        </button>
      </div>
      {newsData.slice(0, 8).map(news => {
        return (
          <>
            <SingleNewsContainer news={news} />
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

// TODO: put as a helper function
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

const SingleNewsContainer = ({ news }) => {
  const link = extractDomain(news.link) // returns host name ie cryptonews.com

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
        {news.date}
      </div>
      <div
        style={{
          fontSize: 12,
          width: "50%",
          marginLeft: "-10%",
          marginRight: "2%",
          flex: 4,
        }}
      >
        {news.title}
      </div>
      <a
        href={news.link}
        target="_blank"
        style={{ color: "rgb(152, 169, 188)", fontSize: 12, flex: 2 }}
      >
        {link}
      </a>
      <div
        style={{
          flex: 1,
          alignItems: "center",
          display: "flex",
          justifyContent: "center",
          border:
            news.sentiment === "Positive"
              ? "1.3px solid #60BC3F"
              : "1.3px solid #DB3E62",
          padding: 5,
          borderRadius: 5,
          color: news.sentiment === "Positive" ? "#60BC3F" : "#DB3E62",
        }}
      >
        {/* {news.sentiment} */}
        Negative
      </div>
    </div>
  )
}

export default LeftSideSection
