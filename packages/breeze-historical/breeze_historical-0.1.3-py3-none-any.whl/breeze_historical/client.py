import os
import json
from datetime import datetime, timedelta
import boto3
from decimal import Decimal
import requests
import brotli
import time
from typing import Dict, List, Optional, Union
from breeze_connect import BreezeConnect
from .exceptions import BreezeHistoricalError
from .breeze_auth import get_api_session
import traceback

class BreezeHistorical:
    def __init__(
        self,
        breeze_creds: Dict[str, str],
        aws_creds: Dict[str, str],
        symbol_map_path: Optional[str] = None,
        verbose: bool = False,
        token_dir: Optional[str] = None
    ):
        """
        Initialize the BreezeHistorical client
        
        Args:
            breeze_creds (dict): Dictionary containing Breeze API credentials
                - api_key: Breeze API key
                - api_secret: Breeze API secret
                - user_id: Breeze user ID (optional for manual auth)
                - password: Breeze password (optional for manual auth)
                - totp_key: TOTP secret key (optional for manual auth)
            aws_creds (dict): Dictionary containing AWS credentials
                - access_key_id: AWS access key ID
                - secret_access_key: AWS secret access key
                - region: AWS region
                - table_name: DynamoDB table name
            symbol_map_path (str, optional): Path to NSE-ICICI symbol mapping JSON file
            verbose (bool): Whether to print progress information
            token_dir (str, optional): Directory to store session token
        """
        self.verbose = verbose
        if self.verbose:
            print("Initializing BreezeHistorical client...")
            
        # Initialize Breeze client with authentication
        api_session = get_api_session(
            api_key=breeze_creds["api_key"],
            api_secret=breeze_creds["api_secret"],
            user_id=breeze_creds.get("user_id"),
            password=breeze_creds.get("password"),
            totp_secret=breeze_creds.get("totp_key"),
            token_dir=token_dir
        )
        
        self.breeze = BreezeConnect(api_key=breeze_creds["api_key"])
        self.breeze.generate_session(
            api_secret=breeze_creds["api_secret"],
            session_token=api_session
        )
        
        # Initialize DynamoDB client
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=aws_creds["access_key_id"],
            aws_secret_access_key=aws_creds["secret_access_key"],
            region_name=aws_creds["region"]
        )
        self.table = self.dynamodb.Table(aws_creds["table_name"])
        
        # Load symbol mapping
        self.symbol_map = {}
        default_map_path = os.path.join(os.path.dirname(__file__), 'symbol_map.json')
        map_path = symbol_map_path or default_map_path
        
        if os.path.exists(map_path):
            if self.verbose:
                print(f"Loading symbol mapping from {map_path}")
            with open(map_path, 'r') as f:
                self.symbol_map = json.load(f)

        # NSE API URLs
        self.nse_base_url = "https://www.nseindia.com"
        self.nse_api_url = f"{self.nse_base_url}/api/historical"
        
        # Initialize session for NSE API calls
        self.nse_session = requests.Session()
        self._init_nse_session()

    def _init_nse_session(self) -> None:
        """Initialize session for NSE API calls with required headers and cookies"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        
        try:
            # First get the cookies from main page
            self.nse_session.headers.update(headers)
            
            # Visit the main page first
            response = self.nse_session.get(self.nse_base_url, headers=headers)
            response.raise_for_status()
            
            # Then visit the FO report page to get additional cookies
            fo_page_url = f"{self.nse_base_url}/report-detail/fo_eq_security"
            response = self.nse_session.get(fo_page_url, headers=headers)
            response.raise_for_status()
            
            # Update headers for API calls
            api_headers = headers.copy()
            api_headers.update({
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": fo_page_url
            })
            self.nse_session.headers = api_headers
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
        except Exception as e:
            raise BreezeHistoricalError(f"Failed to initialize NSE session: {str(e)}")

    def _get_nse_data(self, url: str) -> Dict:
        """Make authenticated request to NSE API"""
        try:
            if self.verbose:
                print(f"\nMaking request to: {url}")
            
            # Make request without compression
            headers = self.nse_session.headers.copy()
            headers.pop("Accept-Encoding", None)  # Remove compression
            
            response = self.nse_session.get(url, headers=headers)
            if self.verbose:
                print(f"Response status: {response.status_code}")
                # print(f"Response headers: {dict(response.headers)}")
                # print(f"Response content: {response.text[:500]}...")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException:
            if self.verbose:
                print("Request failed, reinitializing session...")
            # If request fails, try reinitializing session and retry once
            self._init_nse_session()
            
            # Retry without compression
            headers = self.nse_session.headers.copy()
            headers.pop("Accept-Encoding", None)
            
            response = self.nse_session.get(url, headers=headers)
            if self.verbose:
                print(f"Retry status: {response.status_code}")
                print(f"Retry content: {response.text[:500]}...")
                
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            raise BreezeHistoricalError(f"Failed to fetch data from NSE: {str(e)}")

    def _get_breeze_symbol(self, nse_symbol: str) -> str:
        """Convert NSE symbol to ICICI Direct symbol"""
        if nse_symbol not in self.symbol_map:
            raise BreezeHistoricalError(
                f"Symbol {nse_symbol} not found in mapping. Please add it to symbol_map.json"
            )
        return self.symbol_map[nse_symbol]
    
    def _get_dynamo_key(self, symbol: str, strike: float, option_type: str, 
                        expiry: str, granularity: str) -> str:
        # If strike is a float and is a whole number, convert to int for key
        if isinstance(strike, float) and strike.is_integer():
            strike = int(strike)
        return f"{symbol}#{strike}#{option_type}#{expiry}#{granularity}"
    
    def _get_valid_timestamps(self, start_date: datetime, end_date: datetime, 
                            granularity: str) -> List[datetime]:
        """Generate list of valid timestamps for the given granularity"""
        timestamps = []
        current = start_date
        
        # Map granularity to timedelta
        granularity_map = {
            "1second": timedelta(seconds=1),
            "1minute": timedelta(minutes=1),
            "5minute": timedelta(minutes=5),
            "30minute": timedelta(minutes=30),
            "1day": timedelta(days=1)
        }
        
        delta = granularity_map[granularity]
        
        while current <= end_date:
            # Only include timestamps during market hours (9:15 AM to 3:30 PM)
            if granularity != "1day":
                if current.hour < 9 or (current.hour == 9 and current.minute < 15):
                    current = current.replace(hour=9, minute=15, second=0, microsecond=0)
                elif current.hour > 15 or (current.hour == 15 and current.minute >= 30):
                    current = (current + timedelta(days=1)).replace(hour=9, minute=15, second=0, microsecond=0)
                    continue
            
            timestamps.append(current)
            current += delta
            
        return timestamps
    def _normalize_timestamp(self, ts: str) -> str:
        """Convert any timestamp format to DynamoDB format (YYYY-MM-DD HH:mm:ss)"""
        try:
            # Try parsing different formats
            for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d-%b-%Y", "%d-%b-%Y %H:%M:%S", "%d-%b-%Y"]:
                try:
                    dt = datetime.strptime(ts, fmt)
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
            raise ValueError(f"Could not parse timestamp: {ts}")
        except Exception as e:
            if self.verbose:
                print(f"Error normalizing timestamp {ts}: {str(e)}")
            raise

    def _fetch_from_dynamo(self, contract_id: str, start_ts: str, end_ts: str) -> List[Dict]:
        """
        Fetch data from DynamoDB
        
        Args:
            contract_id (str): Contract ID used as partition key
            start_ts (str): Start timestamp in any common format
            end_ts (str): End timestamp in any common format
            
        Returns:
            List[Dict]: List of items from DynamoDB
        
        Raises:
            BreezeHistoricalError: If no data found for the given date range
            Exception: For other errors

        Sample DynamoDB item:
                {
        "c_id": {
            "S": "NIFTY#21950#CE#2025-04-30#5minute"
        },
        "ts": {
            "S": "2025-04-08 09:20:00"
        },
        "c": {
            "N": "904.4"
        },
        "h": {
            "N": "918"
        },
        "l": {
            "N": "904.4"
        },
        "o": {
            "N": "918"
        },
        "oi": {
            "N": "0"
        },
        "v": {
            "N": "75"
        }
        }
        """
        try:
            # Normalize timestamps to DynamoDB format
            start_ts_norm = self._normalize_timestamp(start_ts)
            end_ts_norm = self._normalize_timestamp(end_ts)
            
            response = self.table.query(
                KeyConditionExpression="#k = :c_id AND #ts BETWEEN :start AND :end",
                ExpressionAttributeNames={
                    "#k": "c_id",  # 'c_id' is the partition key
                    "#ts": "ts"   # 'ts' for clarity
                },
                ExpressionAttributeValues={
                    ":c_id": contract_id,
                    ":start": start_ts_norm,
                    ":end": end_ts_norm
                }
            )
            # if self.verbose:
            #     print('Key: ', contract_id)
            #     print('Start: ', start_ts_norm)
            #     print('End: ', end_ts_norm)
            #     # print(f"DynamoDB response: {response}")

            items = response.get("Items", [])
            if not items:
                # Check if the key exists but no data for date range
                key_check = self.table.query(
                    KeyConditionExpression="#k = :c_id",
                    Limit=1,
                    ExpressionAttributeNames={"#k": "c_id"},
                    ExpressionAttributeValues={":c_id": contract_id}
                )
                if key_check.get("Items"):
                    print(f"[WARN] No data found between {start_ts_norm} and {end_ts_norm} for {contract_id}")
            
            return items
            
        except BreezeHistoricalError:
            raise
        except Exception as e:
            if self.verbose:
                print(f"Error querying DynamoDB: {str(e)}")
                print(f"Query params: c_id={contract_id}, start={start_ts}, end={end_ts}")
            raise

    def _save_to_dynamo(self, items: List[Dict], contract_id: str) -> None:
        """Save items to DynamoDB using batch writer with better error handling"""
        # Convert items to DynamoDB format using list comprehension
        dynamo_items = [{
            "c_id": contract_id,
            "ts": item["datetime"],
            "o": Decimal(str(item["open"])),
            "h": Decimal(str(item["high"])), 
            "l": Decimal(str(item["low"])),
            "c": Decimal(str(item["close"])),
            "v": int(item["volume"]),
            "oi": int(item["open_interest"])
        } for item in items]

        # Deduplicate by (c_id, ts)
        seen = set()
        deduped_items = []
        for item in dynamo_items:
            key = (item["c_id"], item["ts"])
            if key not in seen:
                deduped_items.append(item)
                seen.add(key)

        if not deduped_items:
            if self.verbose:
                print("No items to save to DynamoDB")
            return

        try:
            # Print summary of data being saved
            if self.verbose:
                print("\nData Summary:")
                print(f"Total records: {len(deduped_items)}")
                print('Saving to DynamoDB...')
            # Process in batches of 25 (DynamoDB limit)
            batch_size = 25
            for i in range(0, len(deduped_items), batch_size):
                batch = deduped_items[i:i + batch_size]
                with self.table.batch_writer() as writer:
                    for item in batch:
                        # Convert float values to Decimal for DynamoDB
                        dynamo_item = {
                            k: Decimal(str(v)) if isinstance(v, float) else v 
                            for k, v in item.items()
                        }
                        # Replace contract_id with c_id if present
                        if "contract_id" in dynamo_item:
                            dynamo_item["c_id"] = dynamo_item.pop("contract_id")
                        writer.put_item(Item=dynamo_item)
        except Exception as e:
            print(f"\nError saving to DynamoDB: {str(e)}")
            print("Current data state:")
            print(f"Number of items: {len(deduped_items)}")
            if deduped_items:
                print("Sample item structure:", deduped_items[0])
            print(traceback.format_exc())
            breakpoint()
            raise

    def _fetch_from_breeze(self, symbol: str, strike: int, option_type: str,
                          expiry: str, start_date: str, end_date: str,
                          granularity: str, dev_mode: bool = False) -> List[Dict]:
        """Fetch data from Breeze API"""
        # Convert granularity to Breeze format
        interval_map = {
            "1second": "1second",
            "1minute": "1minute",
            "5minute": "5minute",
            "30minute": "30minute",
            "1day": "1day"
        }
        
        if self.verbose:
            print(f"\nFetching from Breeze API:")
        
        try:
            # Convert dates to ISO format with timezone
            # Normalize to 'YYYY-MM-DD HH:MM:SS' first
            start_norm = self._normalize_timestamp(start_date)
            end_norm = self._normalize_timestamp(end_date)
            # Parse to datetime
            start_dt = datetime.strptime(start_norm, "%Y-%m-%d %H:%M:%S").replace(hour=0, minute=0, second=0)
            end_dt = datetime.strptime(end_norm, "%Y-%m-%d %H:%M:%S").replace(hour=23, minute=59, second=59)
            start_iso = start_dt.isoformat() + ".000Z"
            end_iso = end_dt.isoformat() + ".000Z"
            expiry_iso = datetime.strptime(expiry, "%Y-%m-%d").replace(hour=0, minute=0, second=0).isoformat() + ".000Z"
            

            if option_type.upper() == "FUT":
                if self.verbose:
                    print("Fetching futures data from Breeze API")
                data = self.breeze.get_historical_data_v2(
                    interval=interval_map[granularity],
                    from_date=start_iso,
                    to_date=end_iso,
                    stock_code=symbol,
                    exchange_code='NFO',
                    product_type='futures',
                    expiry_date=expiry_iso,
                    right='others',
                    strike_price=str(0)
                )
                if self.verbose:
                    print("Raw Response:", data)
                    print("Inputs:  ")
                    print(f"Interval: {interval_map[granularity]}")
                    print(f"From: {start_iso}")
                    print(f"To: {end_iso}")
                    print(f"Stock Code: {symbol}")
                    print(f"Exchange Code: NFO")
                    print(f"Product Type: futures")
                    print(f"Expiry Date: {expiry_iso}")
                    print(f"Right: others")
                    print(f"Strike Price: 0")
            else:
                data = self.breeze.get_historical_data_v2(
                    interval=interval_map[granularity],
                    from_date=start_iso,
                    to_date=end_iso,
                    stock_code=symbol,
                    exchange_code='NFO',
                product_type='options',
                expiry_date=expiry_iso,
                right="call" if option_type == "CE" else "put",
                strike_price=str(strike)
            )
            
            # if self.verbose:
            #     # print("Raw Response:", data)
            #     if isinstance(data, dict) and "Success" in data:
            #         print("Data Success:", data["Success"])
            
            if not data or "Success" not in data:
                if self.verbose:
                    print(f"Breeze API Error or No Data:")
                    print(f"Response: {data}")
                return []
                
            if not data["Success"]:
                if self.verbose:
                    print("No data returned from Breeze API")
                    print(f"Response: {data}")
                return []
                
            # Print summary of fetched data
            if self.verbose and data["Success"]:
                print("\nFetched Data Summary:")
                print(f"Total records: {len(data['Success'])}")
                # if data["Success"]:
                #     print("\nFirst 2 records:")
                #     for record in data["Success"][:2]:
                #         print(f"Datetime: {record['datetime']}")
                #         print(f"OHLCV: {record['open']}, {record['high']}, {record['low']}, {record['close']}, {record['volume']}")
                #         print(f"OI: {record['open_interest']}\n")
                        
                #     if len(data["Success"]) > 2:
                #         print("Last 2 records:")
                #         for record in data["Success"][-2:]:
                #             print(f"Datetime: {record['datetime']}")
                #             print(f"OHLCV: {record['open']}, {record['high']}, {record['low']}, {record['close']}, {record['volume']}")
                #             print(f"OI: {record['open_interest']}\n")
                
            return data["Success"]
            
        except Exception as e:
            print(f"\nError fetching from Breeze API: {str(e)}")
            print("Debug info:")
            print(f"URL params: interval={interval_map[granularity]}, from={start_iso}, to={end_iso}")
            print(f"Contract: {symbol} {strike} {option_type} {expiry_iso}")
            if dev_mode:
                breakpoint()
            raise

    def _fetch_from_breeze_compre(self, symbol: str, strike: int, option_type: str,
                                 expiry: str, start_date: str, end_date: str,
                                 granularity: str, dev_mode: bool = False) -> List[Dict]:
        """
        Recursively fetches all data from Breeze API for the given range and granularity, handling the API's row limit.
        Calls _fetch_from_breeze as a helper.
        Returns a list of all records in chronological order.
        """
        # Helper to subtract one granularity step from a datetime
        def subtract_granularity(dt: datetime, granularity: str) -> datetime:
            if granularity == "1second":
                return dt - timedelta(seconds=1)
            elif granularity == "1minute":
                return dt - timedelta(minutes=1)
            elif granularity == "5minute":
                return dt - timedelta(minutes=5)
            elif granularity == "30minute":
                return dt - timedelta(minutes=30)
            elif granularity == "1day":
                return dt - timedelta(days=1)
            else:
                raise ValueError(f"Unknown granularity: {granularity}")

        # Fetch data for the given range
        data = self._fetch_from_breeze(symbol, strike, option_type, expiry, start_date, end_date, granularity, dev_mode=dev_mode)
        if not data or len(data) < 990:
            return data
        # If we have >=990 rows, recursively fetch earlier data
        # Find the earliest timestamp in the result
        try:
            earliest_ts = min(
                [
                    datetime.strptime(item["datetime"], "%Y-%m-%d %H:%M:%S")
                    if len(item["datetime"]) == 19 else
                    datetime.strptime(item["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    for item in data
                ]
            )
        except Exception:
            # Fallback: try parsing with only date
            earliest_ts = min(
                [
                    datetime.strptime(item["datetime"].split("T")[0], "%Y-%m-%d")
                    for item in data
                ]
            )
        # Subtract one granularity step to avoid overlap
        new_end_dt = subtract_granularity(earliest_ts, granularity)
        new_end_str = new_end_dt.strftime("%Y-%m-%d") if granularity == "1day" else new_end_dt.strftime("%Y-%m-%d %H:%M:%S")
        # Only fetch if new_end is after start_date
        if datetime.strptime(start_date, "%Y-%m-%d") < new_end_dt:
            earlier_data = self._fetch_from_breeze_compre(
                symbol, strike, option_type, expiry, start_date, new_end_str, granularity, dev_mode=dev_mode
            )
        else:
            earlier_data = []
        # Combine earlier data and current data, ensuring chronological order
        return (earlier_data or []) + data

    def _fetch_option_data(self, symbol: str, strike: int, option_type: str,
                          expiry: str, start_date: str, end_date: str,
                          granularity: str, dev_mode: bool = False) -> List[Dict]:
        """Check if Option Data is available in DynamoDB, else Fetch from Breeze API and save to DynamoDB and return"""
        contract_id = self._get_dynamo_key(symbol, strike, option_type, expiry, granularity)
        try:
            dynamo_data = self._fetch_from_dynamo(contract_id, start_date, end_date)
        except BreezeHistoricalError as e:
            if "No data found between" in str(e):
                if self.verbose:
                    print(f"Contract exists but no data for date range: {str(e)}")
                return []
            raise
        if dynamo_data:
            if self.verbose:
                print("Data found in DynamoDB!, ",len(dynamo_data),"records found")
            return dynamo_data
        else:
            if self.verbose:
                print("Data not found in DynamoDB, fetching from Breeze API...")
            expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
            start_date_breeze = (expiry_date - timedelta(days=62)).strftime("%Y-%m-%d")
            end_date_breeze = (expiry_date + timedelta(days=1)).strftime("%Y-%m-%d")
            breeze_data = self._fetch_from_breeze_compre(symbol, strike, option_type, expiry, start_date_breeze, end_date_breeze, granularity)
            if self.verbose:
                print("Data fetched from Breeze API, ",len(breeze_data),"records found")
            if len(breeze_data) > 0 and expiry_date < datetime.now():
                self._save_to_dynamo(breeze_data, contract_id)
                if self.verbose:
                    print("Data saved to DynamoDB, fetching from DynamoDB...")
                return self._fetch_from_dynamo(contract_id, start_date, end_date)
            elif len(breeze_data) > 0 and expiry_date >= datetime.now():
                if self.verbose:
                    print("Expiry date is in the future, returning data from Breeze API")
                    # Convert into DynamoDB format
                    dynamo_data = [{
                        "c_id": contract_id,
                        "ts": item["datetime"],
                        "o": Decimal(str(item["open"])),
                        "h": Decimal(str(item["high"])),
                        "l": Decimal(str(item["low"])),
                        "c": Decimal(str(item["close"])),
                        "v": int(item["volume"]),
                        "oi": int(item["open_interest"])
                    } for item in breeze_data]
                return dynamo_data
            else:
                if self.verbose:
                    print("No data returned from Breeze API")
                return []
            
    def _fetch_futures_data(self, symbol: str, start_date: str, end_date: str, expiry: str,
                            granularity: str, dev_mode: bool = False) -> List[Dict]:
        """Fetch futures data from Breeze API"""
        contract_id = self._get_dynamo_key(symbol, 0, "FUT", expiry, granularity)
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
        try:
            dynamo_data = self._fetch_from_dynamo(contract_id, start_date, end_date)
        except BreezeHistoricalError as e:
            if "No data found between" in str(e):
                if self.verbose:
                    print(f"Contract exists but no data for date range: {str(e)}")
                return []
        if dynamo_data:
            if self.verbose:
                print("Data found in DynamoDB!, ",len(dynamo_data),"records found")
            return dynamo_data
        else:
            if self.verbose:
                print("Data not found in DynamoDB, fetching from Breeze API...")
            start_date_breeze = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=90)).strftime("%Y-%m-%d")
            end_date_breeze = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
            breeze_data = self._fetch_from_breeze_compre(symbol, 0, "FUT", expiry, start_date_breeze, end_date_breeze, granularity)
            if self.verbose:
                print("Data fetched from Breeze API, ",len(breeze_data),"records found")
            if len(breeze_data) > 0 and expiry_date < datetime.now():
                self._save_to_dynamo(breeze_data, contract_id)
                return self._fetch_from_dynamo(contract_id, start_date, end_date)
            elif len(breeze_data) > 0 and expiry_date >= datetime.now():
                if self.verbose:
                    print("Expiry date is in the future, returning data from Breeze API")
                    # Convert into DynamoDB format
                    dynamo_data = [{    
                        "c_id": contract_id,
                        "ts": item["datetime"],
                        "o": Decimal(str(item["open"])),
                        "h": Decimal(str(item["high"])),
                        "l": Decimal(str(item["low"])),
                        "c": Decimal(str(item["close"])),
                        "v": int(item["volume"]),
                        "oi": int(item["open_interest"])
                    } for item in breeze_data]
                return dynamo_data
            else:
                if self.verbose:
                    print("No data returned from Breeze API")
                return []
    
   
    def get_nse_stocks(self) -> List[str]:
        """Get list of stocks available for futures trading on NSE"""
        url = f"{self.nse_api_url}/foCPV/meta/symbolv2?instrument=FUTSTK"
        data = self._get_nse_data(url)
        return data.get("symbols", [])

    def get_nse_indices(self) -> List[str]:
        """Get list of indices available for futures trading on NSE"""
        url = f"{self.nse_api_url}/foCPV/meta/symbolv2?instrument=FUTIDX"
        data = self._get_nse_data(url)
        return data.get("symbols", [])

    def get_nse_expiry_dates(self, symbol: str, year: Union[str, int], instrument: str = "OPTIDX") -> List[str]:
        """
        Get list of expiry dates for a given symbol and year
        
        Args:
            symbol (str): Symbol name (e.g., "BANKNIFTY")
            year (str|int): Year (e.g., "2024" or 2024)
            instrument (str): Instrument type ("OPTIDX" for index options, "OPTSTK" for stock options, "FUTIDX" for index futures, "FUTSTK" for stock futures)
            
        Returns:
            List[str]: List of expiry dates in DD-MMM-YYYY format
        """
        url = f"{self.nse_api_url}/foCPV/expireDts?instrument={instrument}&symbol={symbol}&year={year}"
        data = self._get_nse_data(url)
        return data.get("expiresDts", [])

    def get_nse_option_chain(self, symbol: str, from_date: str, to_date: str, 
                           expiry_date: str = None, instrument_type: str = "OPTIDX", 
                           option_type: str = "CE", year: str = None) -> List[Dict]:
        """
        Get option chain data from NSE
        
        Args:
            symbol (str): Symbol name (e.g., "BANKNIFTY")
            from_date (str): Start date in YYYY-MM-DD format
            to_date (str): End date in YYYY-MM-DD format
            expiry_date (str, optional): Expiry date in YYYY-MM-DD format
            instrument_type (str): Instrument type ("OPTIDX" for indices, "OPTSTK" for stocks)
            option_type (str): Option type ("CE" or "PE")
            year (str, optional): Year for historical data
            
        Returns:
            List[Dict]: List of option chain data
        """
        # Convert dates to required format (DD-MM-YYYY)
        from_dt = datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        
        url = f"{self.nse_api_url}/foCPV?from={from_dt}&to={to_dt}&instrumentType={instrument_type}&symbol={symbol}&optionType={option_type}"
        
        # Add optional parameters if provided
        if expiry_date:
            expiry_dt = datetime.strptime(expiry_date, "%Y-%m-%d").strftime("%d-%b-%Y")
            url += f"&expiryDate={expiry_dt}"
        if year:
            url += f"&year={year}"
            
        if self.verbose:
            print(f"\nFetching NSE option chain data...")
            print(f"URL: {url}")
            
        data = self._get_nse_data(url)
        result = data.get("data", [])
        
        if not result and self.verbose:
            print(f"\nNo data returned from NSE API for:")
            print(f"Symbol: {symbol}")
            print(f"From: {from_dt}")
            print(f"To: {to_dt}")
            print(f"Expiry: {expiry_dt if expiry_date else 'Not specified'}")
            print(f"Option Type: {option_type}")
            print("\nTrying to fetch data for a wider date range...")
            
            # Try with a wider date range
            from_wider = (datetime.strptime(from_date, "%Y-%m-%d") - timedelta(days=5)).strftime("%d-%m-%Y")
            to_wider = (datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=5)).strftime("%d-%m-%Y")
            
            url_wider = f"{self.nse_api_url}/foCPV?from={from_wider}&to={to_wider}&instrumentType={instrument_type}&symbol={symbol}&optionType={option_type}"
            if expiry_date:
                url_wider += f"&expiryDate={expiry_dt}"
            if year:
                url_wider += f"&year={year}"
                
            if self.verbose:
                print(f"Trying wider range URL: {url_wider}")
                
            data_wider = self._get_nse_data(url_wider)
            result = data_wider.get("data", [])
            
            if not result and self.verbose:
                print("Still no data available with wider date range")
            elif self.verbose:
                print(f"Found {len(result)} records with wider date range")
        
        return result 

    def get_monthly_expiry(self, expiry_list: list) -> str:
        """
        Given a list of expiry dates in 'DD-MMM-YYYY', return the nearest monthly expiry (last Thursday of the month, or max date in each month).
        Returns the expiry in 'YYYY-MM-DD' format.
        """
        # Convert to datetime
        expiry_dates = [datetime.strptime(e, "%d-%b-%Y") for e in expiry_list]
        # Group by (year, month), pick max (last Thursday) in each month
        monthly_expiries = {}
        for dt in expiry_dates:
            ym = (dt.year, dt.month)
            if ym not in monthly_expiries or dt > monthly_expiries[ym]:
                monthly_expiries[ym] = dt
        # Pick the nearest future expiry (or latest past if all are past)
        today = datetime.now()
        future_expiries = [d for d in monthly_expiries.values() if d >= today]
        if future_expiries:
            nearest = min(future_expiries)
        else:
            nearest = max(monthly_expiries.values())
        return nearest.strftime("%Y-%m-%d")

    def fetch_option_chain_timeseries(self, symbol: str, start_date: str, end_date: str, expiry: str = None, granularity: str = "5minute", option_types: list = ["CE", "PE"]) -> dict:
        """
        Fetches the option chain as a timestamp-centric nested dictionary:
        {timestamp: {expiry: {strike: {option_type: {ohlcvoi+granularity}}}}}
        All timestamps are in 'YYYY-MM-DD HH:MM:SS' format.
        Raises error if symbol or expiry is not found.
        """
        try:
            # 1. Validate symbol
            index_syms = set(self.get_nse_indices())
            stock_syms = set(self.get_nse_stocks())
            if symbol not in index_syms and symbol not in stock_syms:
                raise BreezeHistoricalError(f"Symbol '{symbol}' not found in index or stock options list.")
            # 2. Get expiries for symbol
            year = datetime.strptime(start_date, "%Y-%m-%d").year
            instrument = "OPTIDX" if symbol in index_syms else "OPTSTK"
            expiries = self.get_nse_expiry_dates(symbol, year, instrument)
            if not expiries:
                raise BreezeHistoricalError(f"No expiries found for symbol '{symbol}' in {instrument}.")
            # 3. Validate or select expiry
            if expiry:
                # Accept both 'YYYY-MM-DD' and 'DD-MMM-YYYY' for input
                try:
                    expiry_dt = datetime.strptime(expiry, "%Y-%m-%d")
                    expiry_fmt = expiry_dt.strftime("%d-%b-%Y")
                except ValueError:
                    try:
                        expiry_dt = datetime.strptime(expiry, "%d-%b-%Y")
                        expiry_fmt = expiry
                        expiry = expiry_dt.strftime("%Y-%m-%d")
                    except ValueError:
                        raise BreezeHistoricalError(f"Expiry '{expiry}' is not in a recognized format.")
                if expiry_fmt not in expiries:
                    raise BreezeHistoricalError(f"Expiry '{expiry_fmt}' not found for symbol '{symbol}'.")
            else:
                expiry = self.get_monthly_expiry(expiries)
                expiry_dt = datetime.strptime(expiry, "%Y-%m-%d")
                expiry_fmt = expiry_dt.strftime("%d-%b-%Y")
            # 4. Get all strikes for expiry
            nse_chain = self.get_nse_option_chain(symbol, start_date, end_date, expiry, instrument, "CE", str(expiry_dt.year))
            if not nse_chain:
                raise BreezeHistoricalError(f"No option chain data found for symbol '{symbol}' and expiry '{expiry_fmt}'.")
            # Use float for strikes to avoid merging different strikes
            strikes = sorted(set(float(item["FH_STRIKE_PRICE"]) for item in nse_chain if "FH_STRIKE_PRICE" in item))
            if not strikes:
                raise BreezeHistoricalError(f"No strikes found for symbol '{symbol}' and expiry '{expiry_fmt}'.")
        
            # 5. Fetch data for each strike and option type
            result = {}
            def to_json_serializable(val):
                if isinstance(val, Decimal):
                    if val % 1 == 0:
                        return int(val)
                    else:
                        return float(val)
                return val
            for strike in strikes:
                for opt_type in option_types:
                    if self.verbose:
                        print(f"Fetching data for {symbol} {strike} {opt_type} {expiry} {start_date} {end_date} {granularity}")
                    data = self._fetch_option_data(symbol, strike, opt_type, expiry, start_date, end_date, granularity)
                    for rec in data:
                        ts = self._normalize_timestamp(rec["ts"])  # 'YYYY-MM-DD HH:MM:SS'
                        if ts not in result:
                            result[ts] = {}
                        if expiry not in result[ts]:
                            result[ts][expiry] = {}
                        if strike not in result[ts][expiry]:
                            result[ts][expiry][strike] = {}
                        result[ts][expiry][strike][opt_type] = {
                            "o": to_json_serializable(rec["o"]),
                            "h": to_json_serializable(rec["h"]),
                            "l": to_json_serializable(rec["l"]),
                            "c": to_json_serializable(rec["c"]),
                            "v": to_json_serializable(rec["v"]),
                            "oi": to_json_serializable(rec["oi"]),
                            "granularity": granularity
                        } 
            import json
            return json.dumps(result)
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("\nTraceback:")
            traceback.print_exc()
            breakpoint()
            raise