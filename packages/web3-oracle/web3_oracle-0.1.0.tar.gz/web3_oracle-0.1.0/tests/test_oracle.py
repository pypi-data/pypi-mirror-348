#!/usr/bin/env python3
"""
Unit tests for the web3_oracle package
"""

import unittest
import os
import tempfile
import shutil
from datetime import datetime
import pandas as pd
import pytz
from pathlib import Path

from web3_oracle import Oracle

class TestOracle(unittest.TestCase):
    """Test cases for the Oracle class"""
    
    def setUp(self):
        """Set up test environment with temporary data files"""
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = Path(self.temp_dir) / 'data'
        self.data_dir.mkdir(exist_ok=True)
        
        # Create sample token addresses CSV
        token_addresses = pd.DataFrame({
            'address': [
                '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',
                '0xdac17f958d2ee523a2206206994597c13d831ec7'
            ],
            'symbol': ['ETH', 'BTC', 'USDT'],
            'name': ['Ethereum', 'Bitcoin', 'Tether'],
            'price_file': ['eth_prices.csv', 'btc_prices.csv', 'usdt_prices.csv']
        })
        token_addresses.to_csv(self.data_dir / 'token_addresses.csv', index=False)
        
        # Create sample ETH price data
        eth_prices = pd.DataFrame({
            'timestamp': [1609459200, 1610496000, 1611532800, 1612569600, 1613606400],
            'price': [730.37, 1150.42, 1380.25, 1630.12, 1940.75],
            'volume': [12345678, 23456789, 34567890, 45678901, 56789012]
        })
        eth_prices.to_csv(self.data_dir / 'eth_prices.csv', index=False)
        
        # Create sample BTC price data
        btc_prices = pd.DataFrame({
            'timestamp': [1609459200, 1610496000, 1611532800, 1612569600, 1613606400],
            'price': [29374.15, 37559.03, 32250.45, 38789.12, 51458.65],
            'volume': [98765432, 87654321, 76543210, 65432109, 54321098]
        })
        btc_prices.to_csv(self.data_dir / 'btc_prices.csv', index=False)
        
        # Create sample USDT price data
        usdt_prices = pd.DataFrame({
            'timestamp': [1609459200, 1610496000, 1611532800, 1612569600, 1613606400],
            'price': [1.0, 1.0, 1.0, 1.0, 1.0],
            'volume': [123456789, 234567890, 345678901, 456789012, 567890123]
        })
        usdt_prices.to_csv(self.data_dir / 'usdt_prices.csv', index=False)
        
        # Initialize the oracle with the test data directory
        self.oracle = Oracle(data_dir=self.data_dir)
    
    def tearDown(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir)
    
    def test_token_mapping_loaded(self):
        """Test that token mapping is loaded correctly"""
        self.assertEqual(len(self.oracle.token_mapping), 3)
        self.assertIn('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', self.oracle.token_mapping)
        self.assertEqual(self.oracle.token_mapping['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2']['symbol'], 'ETH')
    
    def test_get_price_exact_timestamp(self):
        """Test getting price at an exact timestamp"""
        # ETH price at timestamp 1610496000 should be 1150.42
        price = self.oracle.get_price('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1610496000)
        self.assertEqual(price, 1150.42)
    
    def test_get_price_between_timestamps(self):
        """Test getting price between timestamps (should return closest)"""
        # Timestamp 1610000000 is between 1609459200 and 1610496000, closer to 1610496000
        price = self.oracle.get_price('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1610000000)
        self.assertEqual(price, 1150.42)
        
        # Timestamp 1609800000 is between 1609459200 and 1610496000, closer to 1609459200
        price = self.oracle.get_price('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1609800000)
        self.assertEqual(price, 730.37)
    
    def test_get_price_before_first_timestamp(self):
        """Test getting price before first timestamp (should return earliest)"""
        price = self.oracle.get_price('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1600000000)
        self.assertEqual(price, 730.37)
    
    def test_get_price_after_last_timestamp(self):
        """Test getting price after last timestamp (should return latest)"""
        price = self.oracle.get_price('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 1620000000)
        self.assertEqual(price, 1940.75)
    
    def test_get_price_by_datetime(self):
        """Test getting price by datetime"""
        dt = datetime(2021, 1, 15, 0, 0, 0)
        price = self.oracle.get_price_by_datetime('0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', dt)
        self.assertEqual(price, 37559.03)
    
    def test_get_price_by_datetime_timezone_aware(self):
        """Test getting price by timezone-aware datetime"""
        dt = datetime(2021, 1, 15, 0, 0, 0, tzinfo=pytz.UTC)
        price = self.oracle.get_price_by_datetime('0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', dt)
        self.assertEqual(price, 37559.03)
    
    def test_get_token_info(self):
        """Test getting token info"""
        info = self.oracle.get_token_info('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
        self.assertEqual(info['symbol'], 'ETH')
        self.assertEqual(info['name'], 'Ethereum')
    
    def test_nonexistent_token(self):
        """Test getting price for nonexistent token"""
        price = self.oracle.get_price('0x1234567890abcdef1234567890abcdef12345678', 1610496000)
        self.assertIsNone(price)
    
    def test_get_available_tokens(self):
        """Test getting available tokens"""
        tokens = self.oracle.get_available_tokens()
        self.assertEqual(len(tokens), 3)
        self.assertTrue(all(key in tokens for key in [
            '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
            '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',
            '0xdac17f958d2ee523a2206206994597c13d831ec7'
        ]))
        self.assertEqual(tokens['0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2']['symbol'], 'ETH')


if __name__ == '__main__':
    unittest.main() 