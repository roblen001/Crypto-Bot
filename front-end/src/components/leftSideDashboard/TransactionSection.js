import React, { useState, useEffect } from "react"
import axios from "axios"
import * as Icon from "react-cryptocoins"
import moment from "moment"

const cryptoIcons = [
  { symbol: "ETH", icon: <Icon.Eth color="white" /> },
  { symbol: "LTC", icon: <Icon.Ltc color="white" /> },
  { symbol: "XRP", icon: <Icon.Xrp color="white" /> },
  { symbol: "BTC", icon: <Icon.Btc color="white" /> },
]

// TODO: restrict the amount of transactions being called on this page
const TransactionSection = () => {
  // fectching transaction history from flask api
  const [transactionHistory, setTransactionHistory] = useState([])

  async function fetchData() {
    try {
      const response = await axios.get(
        // limit this to 10 so it can fit in container
        "http://127.0.0.1:5000/all_transaction_history/10"
      )
      let data = response.data
      setTransactionHistory(data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  console.log(transactionHistory)
  return (
    <div
      style={{
        // border: "1.3px solid rgba(232,236,239,0.2)",
        flex: 1,
        maxHeight: "50%",
        alignItems: "center",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
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
        Transaction History
      </p>
      <div
        style={{
          backgroundColor: "rgba(232,236,239,0.2)",
          width: "100%",
          height: 2,
        }}
      ></div>
      {transactionHistory.map(transaction => {
        return (
          <>
            <SingleTransactionContainer
              key={transaction.id}
              transaction={transaction}
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
  )
}

const SingleTransactionContainer = ({ transaction }) => {
  const icon_name = transaction.symbol.substring(0, 3)

  return (
    <div
      style={{
        width: "100%",
        flexDirection: "row",
        display: "flex",
        height: 60,
        alignItems: "center",
        justifyContent: "space-evenly",
      }}
    >
      {/* Symbol icon and name */}
      {cryptoIcons.map(item => {
        if (item.symbol === icon_name) {
          return item.icon
        }
      })}
      <div style={{ color: "white" }}>{transaction.symbol}</div>
      {/* Price */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div
          style={{
            color: "white",
            fontSize: 12,
          }}
        >
          {transaction.price_with_fee.toFixed(2)}
        </div>
        <div style={{ color: "#98A9BC", fontSize: 12 }}>Price</div>
      </div>
      {/* Quantity */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div
          style={{
            color: "white",
            fontSize: 12,
          }}
        >
          {parseFloat(transaction.qty).toFixed(2)}
        </div>
        <div style={{ color: "#98A9BC", fontSize: 12 }}>qty</div>
      </div>
      {/* date and time */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div
          style={{
            color: "white",
            fontSize: 12,
          }}
        >
          {moment
            .unix(transaction.timestamp / 1000)
            .format("DD MMM YYYY hh:mm a")}
        </div>
        <div style={{ color: "#98A9BC", fontSize: 12 }}>date and time</div>
      </div>
      {/* gain and loss percent*/}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        {transaction.profits === "---" && (
          <div
            style={{
              color: "white",
              fontSize: 12,
            }}
          >
            {transaction.profits} ({transaction.profits_percent}%)
          </div>
        )}
        {transaction.profits != "---" && (
          <div
            style={{
              color: "white",
              fontSize: 12,
            }}
          >
            {parseFloat(transaction.profits).toFixed(2)} (
            {parseFloat(transaction.profits_percent).toFixed(2)}%)
          </div>
        )}
        <div style={{ color: "#98A9BC", fontSize: 12 }}>gains/losses</div>
      </div>
      {/* date and time */}
      <div
        style={{ flexDirection: "row", display: "flex", alignItems: "center" }}
      >
        <div
          style={{
            width: 10,
            height: 10,
            backgroundColor:
              transaction.side === "SELL" ? "#60BC3F" : "#DB3E62",
            borderRadius: 25,
            marginRight: 5,
          }}
        ></div>
        {transaction.side == "BUY" && (
          <div style={{ color: "white", fontSize: 12 }}>BUY</div>
        )}
        {transaction.side == "SELL" && (
          <div style={{ color: "white", fontSize: 12 }}>SELL</div>
        )}
      </div>
    </div>
  )
}

export default TransactionSection
