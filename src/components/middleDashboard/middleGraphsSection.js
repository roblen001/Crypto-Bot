import React, { useState } from "react"
import TradingViewWidget from "react-tradingview-widget"

import "bootstrap/dist/css/bootstrap.min.css"

import "./middleGraphsSection.css"

const MiddleGraphsSection = () => {
  const [symbol, setSymbol] = useState("BTC")

  return (
    <>
      {/* bar graph for live market section */}
      <div style={{ flex: 10, display: "flex", flexDirection: "column" }}>
        {/* top header */}
        <TopHeaderSection setSymbol={setSymbol} symbol={symbol} />
        {/* Chart */}
        <ChartSection symbol={symbol} />
      </div>
      {/* bot forecast graph section */}
      <div style={{ flex: 8 }}></div>
    </>
  )
}

// Top header section
const TopHeaderSection = ({ setSymbol, symbol }) => {
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
          <option value="BINANCE:BTCUSD">BTC/USD</option>
          <option value="BINANCE:ETHUSD">ETH/USD</option>
          <option value="BINANCE:XRPUSD">XRP/USD</option>
        </select>
      </div>
      <div className="dataContainer">
        <text className="greyText">Last Price</text>
        <text className="text">51,952.36</text>
      </div>
      <div className="dataContainer">
        <text className="greyText">24h Change</text>
        <div style={{ display: "flex", flexDirection: "row" }}>
          <text className="text">924.19</text>
          <text style={{ marginLeft: 8, color: "white" }}>+1.42%</text>
        </div>
      </div>
      <div className="dataContainer">
        <text className="greyText">24h High</text>
        <text className="text">52,342.36</text>
      </div>
      <div className="dataContainer">
        <text className="greyText">24h Low</text>
        <text className="text">50,090.06</text>
      </div>
    </div>
  )
}

// chart section
const ChartSection = ({ symbol }) => {
  return (
    <div style={{ flex: 10 }}>
      <TradingViewWidget
        symbol={symbol}
        autosize
        theme="dark"
        studies={["MACD@tv-basicstudies", "MOM@tv-basicstudies"]}
      />
      {symbol}
    </div>
  )
}
export default MiddleGraphsSection
