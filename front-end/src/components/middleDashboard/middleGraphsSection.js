import React, { useState, useEffect } from "react";
import Binance from "binance-api-node";
import styled from "styled-components";
import MenuCard from "./MenuCard";
import TradingViewWidget from "./TradingViewWidget"; // Import the TradingViewWidget component

const client = Binance();

const MiddleGraphsSection = () => {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [dailyStatsForSymbol, setDailyStatsForSymbol] = useState({});

  useEffect(() => {
    client.dailyStats({ symbol }).then(stat => {
      setDailyStatsForSymbol(stat);
    }).catch(error => {
      console.error('Error fetching daily stats:', error);
    });
  }, [symbol]);

  const dailyHigh = parseFloat(dailyStatsForSymbol.highPrice || 0).toFixed(2);
  const dailyLow = parseFloat(dailyStatsForSymbol.lowPrice || 0).toFixed(2);
  const priceChangePercent = dailyStatsForSymbol.priceChangePercent || 0;
  const priceChange = parseFloat(dailyStatsForSymbol.priceChange || 0).toFixed(2);
  const lastPrice = parseFloat(dailyStatsForSymbol.lastPrice || 0).toFixed(2);

  return (
    <Section>
      <TopHeaderSection
        setSymbol={setSymbol}
        symbol={symbol}
        dailyHigh={dailyHigh}
        dailyLow={dailyLow}
        priceChangePercent={priceChangePercent}
        lastPrice={lastPrice}
        priceChange={priceChange}
      />
      <ChartSection symbol={symbol} />
      <MenuCardSection>
        <MenuCard />
      </MenuCardSection>
    </Section>
  );
};

const TopHeaderSection = ({
  setSymbol,
  symbol,
  dailyHigh,
  dailyLow,
  priceChangePercent,
  lastPrice,
  priceChange,
}) => {
  const handleTabChange = tab => {
    setSymbol(tab);
  };

  return (
    <Header>
      <ToggleSwitch>
        <ToggleOption
          active={symbol === "BTCUSDT"}
          onClick={() => handleTabChange("BTCUSDT")}
        >
          BTC/USD
        </ToggleOption>
        <ToggleOption
          active={symbol === "ETHUSDT"}
          onClick={() => handleTabChange("ETHUSDT")}
        >
          ETH/USD
        </ToggleOption>
        <ToggleOption
          active={symbol === "XRPUSDT"}
          onClick={() => handleTabChange("XRPUSDT")}
        >
          XRP/USD
        </ToggleOption>
      </ToggleSwitch>
      <DataContainer>
        <DataCard>
          <GreyText>Last Price</GreyText>
          <DataText
            style={{ color: priceChangePercent >= 0 ? "#60BC3F" : "#DB3E62" }}
          >
            {lastPrice}
          </DataText>
        </DataCard>
        <DataCard>
          <GreyText>24h Change</GreyText>
          <DataChange>
            <DataText
              style={{ color: priceChangePercent >= 0 ? "#60BC3F" : "#DB3E62" }}
            >
              {priceChange}
            </DataText>
            <div>
              {priceChangePercent >= 0 && (
                <ChangeSymbol style={{ color: "#60BC3F" }}>+</ChangeSymbol>
              )}
              <DataText
                style={{
                  color: priceChangePercent >= 0 ? "#60BC3F" : "#DB3E62",
                }}
              >
                {priceChangePercent}%
              </DataText>
            </div>
          </DataChange>
        </DataCard>
        <DataCard>
          <GreyText>24h High</GreyText>
          <DataText>{dailyHigh}</DataText>
        </DataCard>
        <DataCard>
          <GreyText>24h Low</GreyText>
          <DataText>{dailyLow}</DataText>
        </DataCard>
      </DataContainer>
    </Header>
  );
};

const ChartSection = ({ symbol }) => {
  return symbol ? <TradingViewWidget symbol={symbol} /> : null;
};

export default MiddleGraphsSection;

const Section = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 0px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  font-family: "Roboto", sans-serif;
`;

const Header = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
`;

const ToggleSwitch = styled.div`
  display: flex;
  background-color: #f0f0f0;
  border-radius: 20px;
  padding: 5px;
  margin-bottom: 20px;
`;

const ToggleOption = styled.div`
  padding: 10px 20px;
  border-radius: 15px;
  cursor: pointer;
  background-color: ${props => (props.active ? "#ffffff" : "transparent")};
  box-shadow: ${props => (props.active ? "0 2px 4px rgba(0, 0, 0, 0.1)" : "none")};
  color: ${props => (props.active ? "#007AFF" : "#777")};
  font-weight: ${props => (props.active ? "bold" : "normal")};
`;

const DataContainer = styled.div`
  display: flex;
  justify-content: space-around;
  width: 100%;
`;

const DataCard = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 10px;
`;

const GreyText = styled.span`
  color: #777;
  font-size: 14px;
`;

const DataText = styled.span`
  color: #333;
  font-size: 18px;
  font-weight: bold;
`;

const DataChange = styled.div`
  display: flex;
  align-items: center;
`;

const ChangeSymbol = styled.span`
  font-size: 18px;
  margin-right: 5px;
`;

const ChartContainer = styled.div`
  width: 100%;
  height: 400px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
`;

const MenuCardSection = styled.div`
  width: 100%;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 15px;
  height: 550px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  font-family: "Roboto", sans-serif;
`;
