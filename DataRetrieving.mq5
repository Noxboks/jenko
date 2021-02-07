//+------------------------------------------------------------------+
//|                                               DataRetrieving.mq5 |
//|                        Copyright 2020, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2020, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int filehandle;
int OnInit()
  {
//---
      ResetLastError();
      filehandle=FileOpen("test_4.csv",FILE_WRITE|FILE_CSV);
      
      if(filehandle!=INVALID_HANDLE) {
         Print("File opened correctly");
      } else {
         Print("Error in opening file, ",GetLastError());
      }
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                       |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
      FileClose(filehandle);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                       |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
     if(newCandleOrNot()==true) {
      Comment("New candle");
      MqlRates PriceInfo[];
      ArraySetAsSeries(PriceInfo, true);
      int PriceData = CopyRates(_Symbol, _Period, 0, 3, PriceInfo);
      
      
      double price_open = PriceInfo[1].open;
      double price_high = PriceInfo[1].high;
      double price_low = PriceInfo[1].low;
      double price_close = PriceInfo[1].close;
      double tick_volume = PriceInfo[1].tick_volume;
      
      string values = TimeToString(PriceInfo[1].time)+
      ","+DoubleToString(price_open)+
      ","+DoubleToString(price_high)+
      ","+DoubleToString(price_low)+
      ","+DoubleToString(price_close)+
      ","+DoubleToString(tick_volume);
      FileWrite(filehandle,values);

     } else {
          Comment("Old candle");
     }
  }
//+------------------------------------------------------------------+

bool newCandleOrNot() {
   MqlRates priceData[];
   bool newCandle = false;
   ArraySetAsSeries(priceData,true);
   CopyRates(_Symbol,_Period,0,3,priceData);
   static int candleCounter;
   static datetime timeStampLastCheck;
   datetime timeStampCurrentCandle;
   timeStampCurrentCandle=priceData[0].time;
   
   if(timeStampCurrentCandle != timeStampLastCheck) {
      timeStampLastCheck=timeStampCurrentCandle;
      candleCounter=candleCounter+1;
      newCandle=true;
   }
   
   return newCandle;
}