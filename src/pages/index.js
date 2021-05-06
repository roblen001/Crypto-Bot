import * as React from "react"
import { Link } from "gatsby"
import { StaticImage } from "gatsby-plugin-image"

import "./styles/index.css"

import Layout from "../components/layout"
import Seo from "../components/seo"
import MiddleGraphsSection from "../components/middleDashboard/middleGraphsSection"

const IndexPage = () => (
  <>
    <Seo title="Home" />
    <div class="wrapper">
      {/* left side of dashboard */}
      <div className="sideColumnWrapper">
        {/* transaction section */}
        <div style={{ flex: 1 }}></div>
        {/* news and sentiment analysis section */}
        <div style={{ flex: 1 }}></div>
      </div>
      {/* middle of dashboard */}
      <div className="middleColumnWrapper">
        <MiddleGraphsSection />
      </div>
      {/* right side of dashboard */}
      <div className="sideColumnWrapper">
        {/* user inputs section */}
        <div style={{ flex: 1 }}></div>
        {/* account information ie Balance and gains section */}
        <div style={{ flex: 1 }}></div>
      </div>
    </div>
  </>
)

export default IndexPage
