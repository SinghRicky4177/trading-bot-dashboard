# stock_lists.py

# Top 100 US stocks by volume (quick, high liquidity)
US_STOCKS = [
    'AAPL','MSFT','GOOGL','AMZN','NVDA','META','TSLA','V','ADBE','BAC',
    'AVGO','TXN','PLD','C','JPM','WMT','KO','PEP','NFLX','AMD','INTC',
    'CSCO','QCOM','IBM','ORCL','CRM','PYPL','DIS','COST','HD','NKE','MRK',
    'ABBV','TMO','ACN','NEE','DHR','LOW','SBUX','UPS','BA','CAT','UNP','GE',
    'GS','BLK','AXP','RTX','LMT','DE','F','CMCSA','PFE','ABT','NVS','AZN',
    'TMUS','UBER','NOW','INTU','ISRG','REGN','VRTX','MRNA','ILMN','IDXX','DXCM',
    'WDAY','PANW','SNPS','CDNS','ADSK','ROP','IT','FTNT','OKTA','DDOG','NET',
    'ZS','CRWD','SPLK','TEAM','DOCU','ZM','ROKU','TTD','PINS','SNAP','TWLO',
    'RBLX','U','COIN','SQ','SHOP','SE','PDD','BABA','JD','NTES','BIDU'
]

# Top 100 Canadian stocks (TSX)
CANADIAN_STOCKS = [
    'RY.TO','TD.TO','ENB.TO','CNQ.TO','BNS.TO','BMO.TO','CM.TO','SHOP.TO',
    'SU.TO','CVE.TO','MFC.TO','SLF.TO','GIB.A.TO','T.TO','BCE.TO','RCI.B.TO',
    'NA.TO','IMO.TO','K.TO','CNR.TO','CP.TO','WCN.TO','ATD.TO','DOL.TO','L.TO',
    'MRU.TO','WN.TO','NTR.TO','AGU.TO','ABX.TO','FNV.TO','WPM.TO','AEM.TO',
    'PAAS.TO','TFII.TO','CSU.TO','TOI.TO','BYD.TO','QBR.B.TO','FSV.TO','OTEX.TO',
    'BB.TO','AC.TO','TRP.TO','PPL.TO','H.TO','FTS.TO','EMA.TO','ALA.TO','BIP.UN.TO',
    'BEP.UN.TO','NET.UN.TO','CAR.UN.TO','CPX.TO','RUS.TO','SAP.TO','TRI.TO','GWO.TO',
    'IGM.TO','POW.TO','X.TO','Y.TO','Z.TO','WSP.TO','STN.TO','ARE.TO','CIGI.TO'
]

# Combine both for "all markets"
ALL_STOCKS = US_STOCKS + CANADIAN_STOCKS

print(f"Loaded {len(US_STOCKS)} US stocks, {len(CANADIAN_STOCKS)} Canadian stocks, total {len(ALL_STOCKS)}")
