import pandas as pd
from datetime import timezone, datetime, date
from typing import Optional, Union
import polygon
import os
import dotenv

dotenv.load_dotenv()


def take_polygon_gold_historical_data(
  from_: Union[str, int, datetime, date],
  to: Union[str, int, datetime, date],
  candle_size: int,
  api_key: str,
  limit: Optional[int] = None,
  tz: timezone = timezone.utc,
) -> pd.DataFrame:
  client = polygon.RESTClient(api_key=api_key)
  aggs = []
  for a in client.list_aggs(ticker=f'{symbol}', multiplier=candle_size, timespan="minute", from_=from_, to=to, limit=limit):
    data = {
      "Time": datetime.fromtimestamp(a.timestamp / 1000, tz=tz),
      "Open": a.open,
      "High": a.high,
      "Low": a.low,
      "Close": a.close,
      "Volume": a.volume
    }
    aggs.append(data)
  print(aggs)
  df = pd.DataFrame(aggs)
  df.set_index("Time", inplace=True)
  return df

if __name__ == "__main__":
  api_key = os.getenv("POLYGON_API_KEY")
  symbol = "C:XAUUSD"
  candle_size = 30
  tz = timezone.utc
  from_ = "2024-06-01"
  to = "2025-01-01"
  limit = 50000000
  dir_path = f"data/polygon_data/{symbol}/{candle_size}/"
  file_path = f"{from_}_{to}.csv"

  data = take_polygon_gold_historical_data(
  api_key=api_key,
  from_=from_,
  to=to,
  limit=limit,
  candle_size=candle_size,
  tz=tz
  )

  os.makedirs(dir_path, exist_ok=True)
  with open(dir_path + file_path, "w") as fp:
    data.to_csv(fp)
