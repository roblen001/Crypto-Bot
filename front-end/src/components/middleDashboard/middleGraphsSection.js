import React, { useState, useEffect } from "react"
import TradingViewWidget from "react-tradingview-widget"
import Binance from "binance-api-node"

import "bootstrap/dist/css/bootstrap.min.css"

import "./middleGraphsSection.css"

const client = Binance()

// Authenticated client, can make signed calls
const client2 = Binance({
  apiKey: process.env.GATSBY_APIKEY,
  apiSecret: process.env.GATSBY_APISECRET,
})

const MiddleGraphsSection = () => {
  const [symbol, setSymbol] = useState("BTCUSDT")
  const [dailyStatsForSymbol, setDailyStatsForSymbol] = useState(0)

  // getting symbol statistics
  useEffect(() => {
    client.dailyStats({ symbol: symbol }).then(stat => {
      setDailyStatsForSymbol(stat)
    })
  }, [symbol])

  const dailyHigh = parseFloat(dailyStatsForSymbol.highPrice).toFixed(2)
  const dailyLow = parseFloat(dailyStatsForSymbol.lowPrice).toFixed(2)
  const priceChangePercent = dailyStatsForSymbol.priceChangePercent
  const priceChange = parseFloat(dailyStatsForSymbol.priceChange).toFixed(2)
  const lastPrice = parseFloat(dailyStatsForSymbol.lastPrice).toFixed(2)
  return (
    <>
      {/* bar graph for live market section */}
      <div
        style={{
          flex: 10,
          display: "flex",
          flexDirection: "column",
          background: "#3C4C5E",
        }}
      >
        {/* top header */}
        <TopHeaderSection
          setSymbol={setSymbol}
          symbol={symbol}
          setDailyStatsForSymbol={setDailyStatsForSymbol}
          dailyHigh={dailyHigh}
          dailyLow={dailyLow}
          priceChangePercent={priceChangePercent}
          lastPrice={lastPrice}
          priceChange={priceChange}
        />
        {/* Chart */}
        <ChartSection symbol={symbol} />
      </div>
      {/* bot forecast graph section */}
      <div style={{ flex: 8 }}></div>
    </>
  )
}

// Top header section
const TopHeaderSection = ({
  setSymbol,
  symbol,
  setDailyStatsForSymbol,
  dailyHigh,
  dailyLow,
  priceChangePercent,
  lastPrice,
  priceChange,
}) => {
  function handleSelectChange(event) {
    setSymbol(event.target.value)
  }

  return (
    <div
      style={{
        flex: 3,
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-evenly",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          height: "100%",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <select
          className="dropDown"
          value={symbol}
          onChange={handleSelectChange}
        >
          <option value="BTCUSDT">BTC/USD</option>
          <option value="ETHUSDT">ETH/USD</option>
          <option value="XRPUSDT">XRP/USD</option>
        </select>
      </div>
      <div className="dataContainer">
        <text className="greyText">Last Price</text>
        <text
          style={{
            fontSize: 18,
            color: priceChangePercent >= 0 ? "#60BC3F" : "#DB3E62",
          }}
        >
          {lastPrice}
        </text>
      </div>
      <div className="dataContainer">
        <text className="greyText">24h Change</text>
        <div style={{ display: "flex", flexDirection: "row" }}>
          <text
            style={{
              fontSize: 18,
              color: priceChangePercent >= 0 ? "#60BC3F" : "#DB3E62",
            }}
          >
            {priceChange}
          </text>
          <div>
            {priceChangePercent >= 0 && (
              <text style={{ color: "#60BC3F", marginLeft: 8 }}>+</text>
            )}
            <text
              style={{
                marginLeft: priceChangePercent >= 0 ? 0 : 8,
                color: priceChangePercent >= 0 ? "#60BC3F" : "#DB3E62",
              }}
            >
              {priceChangePercent}%
            </text>
          </div>
        </div>
      </div>
      <div className="dataContainer">
        <text className="greyText">24h High</text>
        <text className="text">{dailyHigh}</text>
      </div>
      <div className="dataContainer">
        <text className="greyText">24h Low</text>
        <text className="text">{dailyLow}</text>
      </div>
    </div>
  )
}

// chart section
const ChartSection = ({ symbol }) => {
  return (
    <div
      style={{
        flex: 10,
        paddingLeft: "3%",
        paddingRight: "3%",
        paddingBottom: "3%",
      }}
    >
      <TradingViewWidget
        symbol={symbol}
        autosize
        theme="dark"
        studies={["MACD@tv-basicstudies", "MOM@tv-basicstudies"]}
      />
    </div>
  )
}
export default MiddleGraphsSection
