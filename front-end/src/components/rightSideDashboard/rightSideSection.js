import React, { useState, useEffect } from "react"
import * as Icon from "react-cryptocoins"
import Binance from "binance-api-node"
import axios from "axios"

// svgs
import ArrowGain from "../../images/ArrowGain.svg"
import ArrowLoss from "../../images/ArrowLoss.svg"

// TODO: -only looks for values of USDT
//       -bot will only be able to trade from UDST (might need to be fixed)

const client = Binance()

// Authenticated client, can make signed calls
const client2 = Binance({
  apiKey: process.env.GATSBY_APIKEY,
  apiSecret: process.env.GATSBY_APISECRET,
})

const cryptoIcons = [
  { symbol: "ETH", icon: <Icon.Eth color="white" /> },
  { symbol: "LTC", icon: <Icon.Ltc color="white" /> },
  { symbol: "XRP", icon: <Icon.Xrp color="white" /> },
  { symbol: "BTC", icon: <Icon.Btc color="white" /> },
  { symbol: "USDT", icon: <Icon.Usdt color="white" /> },
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
  // TODO: This needs to be set on the currency that the bot is currently trading
  const [symbol, setSymbol] = useState("BTCUSDT")
  const [netProfits, setNetProfits] = useState(0)
  const [tradesWinRate, setTradesWinRate] = useState(0)
  const [strategyCompare, setStrategyCompare] = useState(0)

  function handleSelectChange(event) {
    setSymbol(event.target.value)
  }

  async function fetchData() {
    try {
      const response1 = await axios.get(
        "http://127.0.0.1:5000/botstatistics/netprofits"
      )
      const response2 = await axios.get(
        "http://127.0.0.1:5000/botstatistics/positivetrades"
      )
      const response3 = await axios.get(
        "http://127.0.0.1:5000/botstatistics/comparestrategy"
      )
      let stat1 = response1.data
      setNetProfits(stat1.toFixed(2))

      let stat2 = response2.data
      setTradesWinRate(stat2.toFixed(2))

      let stat3 = response3.data
      setStrategyCompare(stat3.toFixed(2))
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <>
      {/* feeding station */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <p
          style={{
            marginRight: "60%",
            color: "white",
            marginTop: "2%",
            marginLeft: "5%",
            marginBottom: "1%",
          }}
        >
          Feeding Station
        </p>
        <div
          style={{
            backgroundColor: "rgba(232,236,239,0.2)",
            width: "100%",
            height: 2,
          }}
        ></div>
        {/* input section */}
        <div
          style={{
            height: 50,
            display: "flex",
            flexDirection: "row",
            color: "white",
            alignItems: "center",
            justifyContent: "space-evenly",
            width: "100%",
            paddingLeft: "3%",
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
                marginLeft: "2%",
              }}
            >
              <div>Total Fed:</div>
              <div>100$</div>
            </div>
            <div style={{ color: "white", fontSize: 12, marginLeft: "2%" }}>
              *currency is in USD
            </div>
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              alignItems: "center",
            }}
          >
            <div>Feed The Bot:</div>
            <input
              style={{
                width: "20%",
                marginLeft: "2%",
                marginRight: "2%",
              }}
            />
            <button>Feed</button>
          </div>
        </div>
        <div
          style={{
            backgroundColor: "rgba(232,236,239,0.2)",
            width: "90%",
            height: 2,
          }}
        ></div>
        {mockData2.slice(0, 8).map(transaction => {
          return (
            <>
              <SingleFeedingHistoryContainer
                date={transaction["date"]}
                amount={transaction["amount"]}
              />
              <div
                style={{
                  backgroundColor: "rgba(232,236,239,0.2)",
                  width: "90%",
                  height: 2,
                }}
              ></div>
            </>
          )
        })}
      </div>
      <div
        style={{
          backgroundColor: "rgba(232,236,239,0.2)",
          width: "100%",
          height: 2,
        }}
      ></div>
      {/* account information ie Balance and gains section */}
      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-start",
          flexDirection: "column",
        }}
      >
        {/* User Control Section: This section will override the bot ie KILL SWITCH */}
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
              backgroundColor: "#26374C",
              border: 0,
              color: "white",
              width: "26%",
              fontSize: 25,
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
              justifyContent: "space-evenly",
              width: "70%",
              marginTop: "3%",
              marginBottom: "3%",
            }}
          >
            <button
              style={{
                backgroundColor: "#60BC3F",
                borderRadius: 10,
                width: "30%",
              }}
            >
              Buy
            </button>
            <button
              style={{
                backgroundColor: "#DB3E62",
                borderRadius: 10,
                width: "30%",
              }}
            >
              Sell
            </button>
          </div>
        </div>
        {/* Bot Statistics Section */}
        {/* TODO: these number need to be talking directly to the SQL databse */}
        <div
          style={{
            color: "white",
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-evenly",
            width: "100%",
            marginTop: "5%",
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
                color: netProfits <= 0 ? "#DB3E62" : "#60BC3F",
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
                color: tradesWinRate <= 0 ? "#DB3E62" : "#60BC3F",
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
                color: strategyCompare <= 0 ? "#DB3E62" : "#60BC3F",
              }}
            >
              {strategyCompare}$
            </div>
          </div>
        </div>
        {/* Account Balance Section */}
        <div style={{ color: "white", marginTop: "5%" }}>Account Balance</div>
        {mockData.balances.map(asset => {
          return (
            <>
              <SingleAccountBalance key={asset.asset} asset={asset} />
              <div
                style={{
                  backgroundColor: "rgba(232,236,239,0.2)",
                  width: "80%",
                  height: 1,
                }}
              ></div>
            </>
          )
        })}
      </div>
    </>
  )
}

const SingleAccountBalance = ({ asset }) => {
  const [dailyStatsForSymbol, setDailyStatsForSymbol] = useState(0)
  const symbol = asset.asset + "USDT"

  // getting symbol statistics
  useEffect(() => {
    if (asset.asset != "USDT") {
      client.dailyStats({ symbol: symbol }).then(stat => {
        setDailyStatsForSymbol(stat)
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
          {/* icon */}
          {cryptoIcons.map(item => {
            if (item.symbol === asset.asset) {
              return item.icon
            }
          })}
          {/* symbol */}
          <div style={{ color: "white", marginLeft: "7%" }}>{asset.asset}</div>
        </div>
        {/* quantity */}
        <div
          style={{
            color: "white",
            width: "30%",
            marginRight: "15%",
            display: "flex",
          }}
        >
          <div style={{ marginRight: "3%" }}>
            {parseFloat(asset.free).toFixed(2)}
          </div>
          <div> {asset.asset.toLowerCase()}</div>
        </div>
      </div>
      {priceChangePercent >= 0 && <ArrowGain />}
      {priceChangePercent < 0 && <ArrowLoss />}
      {/* TODO: make sure this is quantiy and not amount in USDT value */}
      {/* valuation */}
      {asset.asset != "USDT" && (
        <div
          style={{
            color: priceChangePercent >= 0 ? "#60BC3F" : "#DB3E62",
            marginLeft: "1%",
          }}
        >
          {(lastPrice * parseFloat(asset.free)).toFixed(2)}
        </div>
      )}
      {asset.asset == "USDT" && (
        <div
          style={{
            color: "white",
            marginLeft: "1%",
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
        color: "white",
        paddingLeft: "2%",
        width: "100%",
        paddingLeft: "8%",
      }}
    >
      {/* icon and symbol */}
      <Icon.Usdt color="white" />
      <div
        style={{
          width: "12%",
          paddingLeft: "1%",
        }}
      >
        USDT
      </div>
      {/* amount */}
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
            color: "white",
            fontSize: 12,
          }}
        >
          {amount}$
        </div>
        <div style={{ color: "#98A9BC", fontSize: 12, marginTop: -4 }}>
          Amount
        </div>
      </div>
      {/* Date */}
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
            color: "white",
            fontSize: 12,
          }}
        >
          {date}
        </div>
        <div style={{ color: "#98A9BC", fontSize: 12, marginTop: -4 }}>
          date and time
        </div>
      </div>
    </div>
  )
}
export default RightSideSection
