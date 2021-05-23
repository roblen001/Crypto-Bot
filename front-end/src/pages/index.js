import * as React from "react"
import { Link } from "gatsby"
import { StaticImage } from "gatsby-plugin-image"

import "./index.css"

import Layout from "../components/layout"
import Seo from "../components/seo"
import MiddleGraphsSection from "../components/middleDashboard/middleGraphsSection"
import LeftSideSection from "../components/leftSideDashboard/leftSideSection"
import RightSideSection from "../components/rightSideDashboard/rightSideSection"

const IndexPage = () => (
  <>
    <Seo title="Home" />
    <div class="wrapper">
      {/* left side of dashboard */}
      <div className="sideColumnWrapper">
        <LeftSideSection />
      </div>
      {/* middle of dashboard */}
      <div className="middleColumnWrapper">
        <MiddleGraphsSection />
      </div>
      {/* right side of dashboard */}
      <div className="sideColumnWrapper">
        <RightSideSection />
      </div>
    </div>
  </>
)

export default IndexPage
