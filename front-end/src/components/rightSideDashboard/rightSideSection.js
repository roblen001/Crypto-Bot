import React, { useState, useEffect } from "react"
import * as Icon from "react-cryptocoins"
import moment from "moment"

// svgs
import ArrowGain from "../../images/ArrowGain.svg"
import ArrowLoss from "../../images/ArrowLoss.svg"
import BNB from "../../images/binance-coin-logo-svg-vector.svg"

const cryptoIcons = [
  { symbol: "ETH", icon: <Icon.Eth color="black" /> },
  { symbol: "LTC", icon: <Icon.Ltc color="black" /> },
  { symbol: "XRP", icon: <Icon.Xrp color="black" /> },
  { symbol: "BTC", icon: <Icon.Btc color="black" /> },
  { symbol: "USDT", icon: <Icon.Usdt color="black" /> },
  { symbol: "ADA", icon: <Icon.Ada color="black" /> },
  {
    symbol: "BNB",
    icon: <BNB style={{ height: 28, width: 28 }} color="black" />,
  },
]

const mockData2 = [
  { amount: 100, date: "11 Oct 2017 08:32 am" },
  { amount: 100, date: "11 Oct 2017 08:32 am" },
  { amount: 200, date: "11 Oct 2017 08:32 am" },
  { amount: 130, date: "11 Oct 2017 08:32 am" },
  { amount: 1450, date: "11 Oct 2017 08:32 am" },
  { amount: 100, date: "11 Oct 2017 08:32 am" },
  { amount: 100, date: "11 Oct 2017 08:32 am" },
  { amount: 200, date: "11 Oct 2017 08:32 am" },
  { amount: 130, date: "11 Oct 2017 08:32 am" },
  { amount: 1450, date: "11 Oct 2017 08:32 am" },
]

const mockData = {
  makerCommission: 15,
  takerCommission: 15,
  buyerCommission: 0,
  sellerCommission: 0,
  canTrade: true,
  canWithdraw: true,
  canDeposit: true,
  balances: [
    {
      asset: "BTC",
      free: "4723846.89208129",
      locked: "0.00000000",
    },
    {
      asset: "LTC",
      free: "4763368.68006011",
      locked: "0.00000000",
    },
    {
      asset: "USDT",
      free: "4763368.68006011",
      locked: "0.00000000",
    },
    {
      asset: "ETH",
      free: "4763368.68006011",
      locked: "0.00000000",
    },
  ],
}

const RightSideSection = () => {
  const [symbol, setSymbol] = useState("BTCUSDT")
  const [netProfits, setNetProfits] = useState(0)
  const [tradesWinRate, setTradesWinRate] = useState(0)
  const [strategyCompare, setStrategyCompare] = useState(0)
  const [botFeederHistoricalData, setBotFeederHistoricalData] = useState([])
  const [totalFed, setTotalFed] = useState(0)
  const [inputData, setInputData] = useState(null)
  const [balance, setBalance] = useState([])

  function handleSelectChange(event) {
    setSymbol(event.target.value)
  }

  useEffect(() => {
    setNetProfits((5000.0).toFixed(2)) // Example net profits
    setTradesWinRate((75.0).toFixed(2)) // Example win rate
    setStrategyCompare((1000.0).toFixed(2)) // Example strategy compare
    setBotFeederHistoricalData(mockData2)
    setTotalFed(12000) // Example total fed
    setBalance(mockData.balances)
  }, [])

  return (
    <div
      style={{ padding: "20px", backgroundColor: "#e0e0e0", height: "100%" }}
    >
      {/* feeding station */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          backgroundColor: "#fff",
          borderRadius: "10px",
          padding: "20px",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          marginBottom: "20px",
          maxHeight: "650px",
          overflowY: "hidden",
          position: "relative",
        }}
      >
        <style>
          {`
            .no-scrollbar::-webkit-scrollbar {
              display: none;
            }
            .no-scrollbar {
              -ms-overflow-style: none;  /* IE and Edge */
              scrollbar-width: none;  /* Firefox */
            }
            .scrollable-content {
              overflow-y: scroll;
              height: 100%;
              padding-right: 10px;
              box-sizing: content-box;
            }
          `}
        </style>
        <p
          style={{
            color: "#333",
            marginTop: "0",
            fontSize: "1.5rem",
            fontWeight: "bold",
            fontFamily: "Arial, sans-serif",
          }}
        >
          Feeding Station
        </p>
        <div
          style={{
            backgroundColor: "#e0e0e0",
            width: "100%",
            height: 2,
            marginBottom: "20px",
          }}
        ></div>
        {/* input section */}
        <div
          style={{
            height: 50,
            display: "flex",
            flexDirection: "row",
            color: "#333",
            alignItems: "center",
            justifyContent: "space-between",
            width: "100%",
          }}
        >
          <div
            style={{
              flexDirection: "column",
              display: "flex",
              width: "50%",
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                fontFamily: "Arial, sans-serif",
              }}
            >
              <div style={{ marginRight: "10px" }}>Total Fed:</div>
              <div>{totalFed}$</div>
            </div>
            <div
              style={{
                fontSize: 12,
                color: "#777",
                fontFamily: "Arial, sans-serif",
              }}
            >
              *currency is in USD
            </div>
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              alignItems: "center",
              fontFamily: "Arial, sans-serif",
            }}
          >
            <div style={{ marginRight: "10px" }}>Feed The Bot:</div>
            <input
              style={{
                width: "60px",
                marginRight: "10px",
                padding: "5px",
                borderRadius: "5px",
                border: "1px solid #ddd",
                fontFamily: "Arial, sans-serif",
              }}
              name="amount"
              type="number"
              value={inputData}
              onChange={e => {
                setInputData(e.target.value)
              }}
            />
            <button
              onClick={() => {
                const currentDate = new Date()
                const timestamp = currentDate.getTime()

                setBotFeederHistoricalData([
                  ...botFeederHistoricalData,
                  { amount: inputData, timestamp: timestamp },
                ])
                setInputData(null)
              }}
              style={{
                backgroundColor: "#28a745",
                border: "none",
                borderRadius: "5px",
                padding: "5px 10px",
                color: "white",
                cursor: "pointer",
                fontFamily: "Arial, sans-serif",
              }}
            >
              Feed
            </button>
          </div>
        </div>
        <div
          style={{
            backgroundColor: "#e0e0e0",
            width: "100%",
            height: 2,
            margin: "20px 0",
          }}
        ></div>
        <div
          className="no-scrollbar scrollable-content"
          style={{ width: "90%" }}
        >
          {botFeederHistoricalData.map((transaction, index) => {
            return (
              <React.Fragment key={index}>
                <SingleFeedingHistoryContainer
                  date={transaction["date"]}
                  amount={transaction["amount"]}
                />
                <div
                  style={{
                    backgroundColor: "#e0e0e0",
                    width: "100%",
                    height: 2,
                  }}
                ></div>
              </React.Fragment>
            )
          })}
        </div>
      </div>

      {/* account information ie Balance and gains section */}
      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-start",
          flexDirection: "column",
          backgroundColor: "#fff",
          borderRadius: "10px",
          padding: "20px",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        }}
      >
        {/* User Control Section */}
        <div
          style={{
            marginTop: "5%",
            width: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <select
            style={{
              backgroundColor: "#fff",
              border: "1px solid #ddd",
              color: "#333",
              width: "30%",
              fontSize: "1rem",
              borderRadius: "5px",
              padding: "5px",
              cursor: "pointer",
              fontFamily: "Arial, sans-serif",
            }}
            value={symbol}
            onChange={handleSelectChange}
          >
            <option value="BTCUSDT">BTC/USD</option>
            <option value="ETHUSDT">ETH/USD</option>
            <option value="XRPUSDT">XRP/USD</option>
          </select>
          <div
            style={{
              flexDirection: "row",
              display: "flex",
              justifyContent: "space-between",
              width: "60%",
              marginTop: "20px",
            }}
          >
            <button
              style={{
                backgroundColor: "#28a745",
                borderRadius: "5px",
                width: "45%",
                padding: "10px",
                color: "white",
                border: "none",
                cursor: "pointer",
                fontWeight: "bold",
                fontFamily: "Arial, sans-serif",
              }}
            >
              Start
            </button>
            <button
              style={{
                backgroundColor: "#dc3545",
                borderRadius: "5px",
                width: "45%",
                padding: "10px",
                color: "white",
                border: "none",
                cursor: "pointer",
                fontWeight: "bold",
                fontFamily: "Arial, sans-serif",
              }}
            >
              Stop
            </button>
          </div>
        </div>

        {/* Bot Statistics Section */}
        <div
          style={{
            color: "#333",
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-evenly",
            width: "100%",
            marginTop: "20px",
            fontFamily: "Arial, sans-serif",
          }}
        >
          <div
            style={{
              alignItems: "center",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div>Net Profits</div>
            <div
              style={{
                color: netProfits <= 0 ? "#dc3545" : "#28a745",
                fontWeight: "bold",
              }}
            >
              {netProfits}$
            </div>
          </div>
          <div
            style={{
              alignItems: "center",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div>% Positive Trades</div>
            <div
              style={{
                color: tradesWinRate <= 0 ? "#dc3545" : "#28a745",
                fontWeight: "bold",
              }}
            >
              {tradesWinRate}%
            </div>
          </div>
          <div
            style={{
              alignItems: "center",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div>Bot vs Buy and Hold</div>
            <div
              style={{
                color: strategyCompare <= 0 ? "#dc3545" : "#28a745",
                fontWeight: "bold",
              }}
            >
              {strategyCompare}$
            </div>
          </div>
        </div>

        {/* Account Balance Section */}
        <div
          style={{
            color: "#333",
            marginTop: "20px",
            fontWeight: "bold",
            fontFamily: "Arial, sans-serif",
          }}
        >
          Account Balance
        </div>
        {balance.map(asset => {
          return (
            <React.Fragment key={asset.asset}>
              <SingleAccountBalance asset={asset} />
              <div
                style={{
                  backgroundColor: "#e0e0e0",
                  width: "80%",
                  height: 1,
                  margin: "10px 0",
                }}
              ></div>
            </React.Fragment>
          )
        })}
      </div>
    </div>
  )
}

const SingleAccountBalance = ({ asset }) => {
  const [dailyStatsForSymbol, setDailyStatsForSymbol] = useState({})
  const symbol = asset.asset + "USDT"

  useEffect(() => {
    if (asset.asset !== "USDT") {
      setDailyStatsForSymbol({
        lastPrice: "50000.00", // Example last price
        priceChangePercent: 2.5, // Example price change percent
      })
    }
  }, [symbol])

  const lastPrice = parseFloat(dailyStatsForSymbol.lastPrice).toFixed(2)
  const priceChangePercent = dailyStatsForSymbol.priceChangePercent

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        height: 40,
        width: "100%",
        paddingLeft: "5%",
        alignItems: "center",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          width: "60%",
          display: "flex",
        }}
      >
        <div
          style={{
            width: "30%",
            display: "flex",
            alignItems: "center",
          }}
        >
          {cryptoIcons.map(item => {
            if (item.symbol === asset.asset) {
              return item.icon
            }
            return null
          })}
          <div style={{ color: "#333", marginLeft: "10px" }}>{asset.asset}</div>
        </div>
        <div
          style={{
            color: "#333",
            width: "30%",
            marginRight: "15%",
            display: "flex",
          }}
        >
          <div style={{ marginRight: "10px" }}>
            {parseFloat(asset.free).toFixed(2)}
          </div>
          <div>{asset.asset.toLowerCase()}</div>
        </div>
      </div>
      {priceChangePercent >= 0 && <ArrowGain />}
      {priceChangePercent < 0 && <ArrowLoss />}
      {asset.asset !== "USDT" && (
        <div
          style={{
            color: priceChangePercent >= 0 ? "#28a745" : "#dc3545",
            marginLeft: "10px",
            fontWeight: "bold",
          }}
        >
          {(lastPrice * parseFloat(asset.free)).toFixed(2)}
        </div>
      )}
      {asset.asset === "USDT" && (
        <div
          style={{
            color: "#333",
            marginLeft: "10px",
          }}
        >
          ---
        </div>
      )}
    </div>
  )
}

const SingleFeedingHistoryContainer = ({ amount, date }) => {
  return (
    <div
      style={{
        height: 53,
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        color: "#333",
        paddingLeft: "8%",
        width: "100%",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <Icon.Usdt color="black" />
      <div
        style={{
          width: "12%",
          paddingLeft: "10px",
        }}
      >
        USDT
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          width: "20%",
          paddingLeft: "20%",
        }}
      >
        <div
          style={{
            color: "#333",
            fontSize: 12,
          }}
        >
          {amount}$
        </div>
        <div style={{ color: "#777", fontSize: 12, marginTop: -4 }}>Amount</div>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          width: "60%",
          justifyContent: "flex-end",
          paddingLeft: "15%",
        }}
      >
        <div
          style={{
            color: "#333",
            fontSize: 12,
          }}
        >
          {moment(date, "DD MMM YYYY hh:mm a").format("DD MMM YYYY hh:mm a")}
        </div>
        <div style={{ color: "#777", fontSize: 12, marginTop: -4 }}>
          date and time
        </div>
      </div>
    </div>
  )
}

export default RightSideSection
