import React, { useEffect, useState } from "react"
import "./statusCheck.css"

const StatusCheck = () => {
  const [status, setStatus] = useState(
    "Checking if the Flask app is running..."
  )
  const [canProceed, setCanProceed] = useState(false)
  const [isOnline, setIsOnline] = useState(false)
  const [showOverlay, setShowOverlay] = useState(true)

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch("http://localhost:5000/")
        if (response.ok) {
          setStatus("Flask app is running successfully!")
          setCanProceed(true)
          setIsOnline(true)
          setShowOverlay(false)
        } else {
          throw new Error("Network response was not ok")
        }
      } catch (error) {
        setStatus("Warning: Flask app is not running!")
        setCanProceed(true)
      }
    }

    checkStatus()
  }, [])

  const handleProceed = () => {
    setShowOverlay(false)
    setTimeout(() => setIsOnline(true), 500) // Match the duration of the fadeOut animation
  }

  return (
    showOverlay && (
      <div className={`overlay ${!showOverlay && "hidden"}`}>
        <div className="overlay-content">
          <p>{status}</p>
          {canProceed && (
            <>
              <p className="sub-warning">The site will not work as expected.</p>
              <button onClick={handleProceed}>Proceed to the site</button>
            </>
          )}
        </div>
      </div>
    )
  )
}

export default StatusCheck
