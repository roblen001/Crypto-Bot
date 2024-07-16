import React, { useState, useEffect } from "react"
import axios from "axios"
import * as Icon from "react-cryptocoins"
import moment from "moment"
import styled from "styled-components"

// Crypto Icons definition
const cryptoIcons = {
  ETH: <Icon.Eth color="black" />,
  LTC: <Icon.Ltc color="black" />,
  XRP: <Icon.Xrp color="black" />,
  BTC: <Icon.Btc color="black" />,
}

const url = "http://localhost:5000/"

const Card = styled.div`
  padding: 20px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out, flex 0.2s ease-in-out,
    height 0.3s ease-in-out;
  margin-bottom: 20px;
  flex: 1;
  overflow: hidden;
`

const Title = styled.h2`
  margin-bottom: 20px;
  color: #333;
`

const Header = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
`

const ToggleContainer = styled.div`
  display: flex;
  align-items: center;
  position: relative;
  width: 120px;
  height: 40px;
  background-color: #e6e6e6;
  border-radius: 20px;
  padding: 5px;
  cursor: pointer;
`

const ToggleSwitch = styled.div`
  position: absolute;
  top: 5px;
  left: ${props => (props.active ? "65px" : "5px")};
  width: 50px;
  height: 30px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  transition: left 0.3s;
`

const ToggleLabel = styled.span`
  font-size: 14px;
  color: ${props => (props.active ? "#007AFF" : "#aaa")};
  z-index: 1;
  flex: 1;
  text-align: center;
`

const NewsItemContainer = styled.a`
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 10px;
  margin-bottom: 10px;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: background-color 0.2s;

  &:hover {
    background-color: #f1f1f1;
  }
`

const NewsDate = styled.div`
  color: #777;
  font-size: 12px;
  flex: 1.5;
`

const NewsTitle = styled.div`
  font-size: 14px;
  flex: 4;
  margin-left: 20px;
  margin-right: 20px;
`

const NewsSentiment = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 5px 10px;
  border-radius: 10px;
  color: ${props =>
    props.positive ? "#60BC3F" : props.negative ? "#DB3E62" : "#777"};
  background-color: ${props =>
    props.positive
      ? "rgba(96,188,63,0.2)"
      : props.negative
      ? "rgba(219,62,98,0.2)"
      : "rgba(119,119,119,0.2)"};
`

const Container = styled.div`
  display: flex;
  flex-direction: column;
  overflow: auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  color: #333;
  font-family: Arial, sans-serif;

  /* Custom scrollbar */
  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: #aaa;
  }
`

const TransactionContainer = styled.div`
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 10px;
  margin-bottom: 10px;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`

const IconContainer = styled.div`
  display: flex;
  align-items: center;
  flex: 1;
`

const Text = styled.div`
  color: #333;
  margin-left: 10px;
`

const InfoLabel = styled.div`
  color: #777;
`

const SideContainer = styled.div`
  display: flex;
  align-items: center;
`

const SideIndicator = styled.div`
  width: 10px;
  height: 10px;
  background-color: ${props => (props.sell ? "#DB3E62" : "#60BC3F")};
  border-radius: 50%;
  margin-right: 5px;
`
const Info = styled.div`
  color: #333;
  font-size: 14px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`

const TransactionSectionContainer = styled(Card)`
  max-height: 590px;
  overflow-y: auto; /* Makes the container vertically scrollable */

  /* Hide the scrollbar for WebKit-based browsers (Chrome, Safari) */
  &::-webkit-scrollbar {
    display: none;
  }

  /* Hide the scrollbar for other browsers */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
`

const NewsSectionContainer = styled(Card)`
  max-height: 590px;
  overflow-y: auto; /* Makes the container vertically scrollable */

  /* Hide the scrollbar for WebKit-based browsers (Chrome, Safari) */
  &::-webkit-scrollbar {
    display: none;
  }

  /* Hide the scrollbar for other browsers */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
`

const MainContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  /* background-color: #f0f2f5; */
  min-height: 100vh;
`

const CardContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  /* max-width: 800px; */
`

const TransactionSection = () => {
  const [transactionHistory, setTransactionHistory] = useState([])

  async function fetchData() {
    try {
      const response = await axios.get(`${url}/all_transaction_history/10`)
      setTransactionHistory(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <Container>
      <Title>Transaction History</Title>
      {transactionHistory.map(transaction => (
        <SingleTransactionContainer
          key={transaction.id}
          transaction={transaction}
        />
      ))}
    </Container>
  )
}

const SingleTransactionContainer = ({ transaction }) => {
  const icon_name = transaction.symbol
  console.log(transaction)
  console.log(icon_name)

  return (
    <TransactionContainer>
      <IconContainer>
        {cryptoIcons[icon_name]}
        <Text>{transaction.symbol}</Text>
      </IconContainer>
      <Info>
        {transaction.price_with_fee.toFixed(2)}
        <InfoLabel>Price</InfoLabel>
      </Info>
      <Info>
        {parseFloat(transaction.qty).toFixed(2)}
        <InfoLabel>Qty</InfoLabel>
      </Info>
      <Info>
        {moment
          .unix(transaction.timestamp / 1000)
          .format("DD MMM YYYY hh:mm a")}
        <InfoLabel>Date & Time</InfoLabel>
      </Info>
      {transaction.side === "SELL" && (
        <Info
          style={{
            color: transaction.profits <= 0 ? "#DB3E62" : "#60BC3F",
          }}
        >
          {transaction.profits === "---"
            ? `${transaction.profits} (${transaction.profits_percent}%)`
            : `${parseFloat(transaction.profits).toFixed(2)}$ (${parseFloat(
                transaction.profits_percent
              ).toFixed(2)}%)`}
          <InfoLabel>Gains/Losses</InfoLabel>
        </Info>
      )}
      <SideContainer>
        <SideIndicator sell={transaction.side === "SELL"} />
        <Info>{transaction.side}</Info>
      </SideContainer>
    </TransactionContainer>
  )
}

const LeftSideSection = () => {
  const [newsFilter, setNewsFilter] = useState("top")
  const [topNews, setTopNews] = useState([])
  const [allNews, setAllNews] = useState([])
  const [newsData, setNewsData] = useState([])

  async function fetchTopNews() {
    try {
      const response = await axios.get(`${url}/news/top/8`)
      let data = response.data
      setTopNews(data)
      setNewsData(data)
    } catch (error) {
      console.error(error)
    }
  }

  async function fetchAllNews() {
    try {
      const response = await axios.get(`${url}/news/all/8`)
      let data = response.data
      setAllNews(data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchTopNews()
    fetchAllNews()
  }, [])

  useEffect(() => {
    if (newsFilter === "top") {
      setNewsData(topNews)
    } else {
      setNewsData(allNews)
    }
  }, [newsFilter, topNews, allNews])

  return (
    <MainContainer>
      <CardContainer>
        <TransactionSectionContainer>
          <TransactionSection />
        </TransactionSectionContainer>
        <NewsSectionContainer>
          <Header>
            <Title>News</Title>
            <ToggleContainer
              onClick={() =>
                setNewsFilter(newsFilter === "top" ? "latest" : "top")
              }
            >
              <ToggleLabel active={newsFilter === "top"}>Top</ToggleLabel>
              <ToggleLabel active={newsFilter === "latest"}>Latest</ToggleLabel>
              <ToggleSwitch active={newsFilter === "latest"} />
            </ToggleContainer>
          </Header>
          {newsData.slice(0, 8).map((news, index) => (
            <NewsItemContainer key={index} href={news.link} target="_blank">
              <NewsDate>
                {moment(news.date).isValid()
                  ? moment(news.date).format("DD MMM YYYY HH:mm, UTC")
                  : news.date}
              </NewsDate>
              <NewsTitle>{news.title}</NewsTitle>
              <NewsSentiment
                positive={news.sentiment === "Positive"}
                negative={news.sentiment === "Negative"}
              >
                {news.sentiment}
              </NewsSentiment>
            </NewsItemContainer>
          ))}
        </NewsSectionContainer>
      </CardContainer>
    </MainContainer>
  )
}

export default LeftSideSection
