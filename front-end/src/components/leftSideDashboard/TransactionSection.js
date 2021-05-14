import React, { useState, useEffect } from "react"
import axios from "axios"
import * as Icon from "react-cryptocoins"
import moment from "moment"

//  mock data: Transaction Histiory response
const transactionHistory = {
  rows: [
    {
      symbol: "LTCBTC",
      orderId: 1,
      clientOrderId: "myOrder1",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "LTCBTC",
      orderId: 1,
      clientOrderId: "myOrder1",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "LTCBTC",
      orderId: 1,
      clientOrderId: "myOrder2",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "SELL",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },

    {
      symbol: "LTCBTC",
      orderId: 1,
      clientOrderId: "myOrder2",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "SELL",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "ETHBTC",
      orderId: 1,
      clientOrderId: "myOrder3",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "LTCBTC",
      orderId: 1,
      clientOrderId: "myOrder2",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "SELL",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "ETHBTC",
      orderId: 1,
      clientOrderId: "myOrder3",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "ETHBTC",
      orderId: 1,
      clientOrderId: "myOrder3",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "ETHBTC",
      orderId: 1,
      clientOrderId: "myOrder3",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "ETHBTC",
      orderId: 1,
      clientOrderId: "myOrder3",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "ETHBTC",
      orderId: 1,
      clientOrderId: "myOrder3",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
    {
      symbol: "ETHBTC",
      orderId: 1,
      clientOrderId: "myOrder3",
      price: "0.1",
      origQty: "1.0",
      executedQty: "0.0",
      status: "NEW",
      timeInForce: "GTC",
      type: "LIMIT",
      side: "BUY",
      stopPrice: "0.0",
      icebergQty: "0.0",
      time: 1499827319559,
    },
  ],
  total: 3,
}

// TODO: restrict the amount of transactions being called on this page
const TransactionSection = () => {
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
      {transactionHistory.rows.slice(0, 10).map(transaction => {
        return (
          <>
            <SingleTransactionContainer
              key={transaction.clientOrderId}
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
  // icon_name is reformatting transaction.symbol to be able to find the appropriate symbol
  const icon_name =
    transaction.symbol.substring(0, 3).toLowerCase().charAt(0).toUpperCase() +
    transaction.symbol.substring(0, 3).toLowerCase().slice(1)

  // const component = string_to_component()
  // const icon_component_in_string_format
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
      <Icon.Ltc color="white" />
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
          {transaction.price}
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
          {transaction.executedQty}
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
          {moment.unix(transaction.time / 1000).format("DD MMM YYYY hh:mm a")}
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
        <div
          style={{
            color: "white",
            fontSize: 12,
          }}
        >
          100$ (12.5%)
        </div>

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
            backgroundColor: transaction.side === "BUY" ? "#60BC3F" : "#DB3E62",
            borderRadius: 25,
            marginRight: 5,
          }}
        ></div>
        <div style={{ color: "white", fontSize: 12 }}>{transaction.side}</div>
      </div>
    </div>
  )
}

export default TransactionSection
