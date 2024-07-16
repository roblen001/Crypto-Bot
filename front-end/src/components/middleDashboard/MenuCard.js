import React, { Component } from "react"

class MenuCard extends Component {
  constructor(props) {
    super(props)
    this.myRef = React.createRef()
  }

  componentDidMount() {
    const script = document.createElement("script")
    script.src =
      "https://s3.tradingview.com/external-embedding/embed-widget-screener.js"
    script.async = false
    script.innerHTML = JSON.stringify({
      width: "100%",
      height: "99%",
      defaultColumn: "overview",
      screener_type: "crypto_mkt",
      displayCurrency: "USD",
      colorTheme: "light",
      locale: "en",
      isTransparent: false,
    })
    this.myRef.current.appendChild(script)
  }

  render() {
    return (
      <div className="tradingview-widget-container" style={{ height: "400px"}} ref={this.myRef}>
        <div className="tradingview-widget-container__widget"></div>
      </div>
    )
  }
}

export default MenuCard
