#!/usr/bin/env python3
"""
Unit tests for the enhanced features of web3_oracle package
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

class TestOracleEnhanced(unittest.TestCase):
    """Test cases for the enhanced Oracle class features"""
    
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
                '0xdac17f958d2ee523a2206206994597c13d831ec7',
                '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'
            ],
            'symbol': ['ETH', 'BTC', 'USDT', 'UNI'],
            'name': ['Ethereum', 'Bitcoin', 'Tether', 'Uniswap'],
            'price_file': ['eth_prices.csv', 'btc_prices.csv', 'usdt_prices.csv', 'usdt_prices.csv']
        })
        token_addresses.to_csv(self.data_dir / 'token_addresses.csv', index=False)
        
        # Create sample ETH price data
        eth_prices = pd.DataFrame({
            'timestamp': [1609459200, 1610496000, 1611532800, 1612569600, 1613606400],
            'price': [730.37, 1150.42, 1380.25, 1630.12, 1940.75],
            'volume': [12345678, 23456789, 34567890, 45678901, 56789012]
        })
        eth_prices.to_csv(self.data_dir / 'eth_prices.csv', index=False)
        
        # Create sample reference prices
        reference_prices = pd.DataFrame({
            'address': [
                '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',
                '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'
            ],
            'price': [2430.53, 102269.68, 6.64],
            'timestamp': [
                '2025-05-13T05:28:10.619768',
                '2025-05-13T05:28:10.619768',
                '2025-05-13T05:28:10.619768'
            ]
        })
        reference_prices.to_csv(self.data_dir / 'altcoins_prices.csv', index=False)
        
        # Create block to timestamp mapping
        block_timestamps = pd.DataFrame({
            'block_number': [
                10000000, 11000000, 12000000, 13000000, 14000000, 15000000, 
                16000000, 17000000, 18000000, 18030000, 18040000, 19000000, 
                19300000, 19310000
            ],
            'timestamp': [
                1588627320, 1601039370, 1613453410, 1625867450, 1638281490, 1650695530,
                1663109570, 1676323620, 1694463820, 1694723820, 1694983820, 1712604020,
                1717400000, 1718000000
            ]
        })
        block_timestamps.to_csv(self.data_dir / 'eth_block_timestamps.csv', index=False)
        
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
    
    def test_get_reference_price(self):
        """Test getting reference price for a token"""
        # Test with a token that has reference price
        price = self.oracle.get_reference_price('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984')
        self.assertEqual(price, 6.64)
        
        # Test with a token that doesn't have reference price
        price = self.oracle.get_reference_price('0x111111111111111111111111111111111111111')
        self.assertIsNone(price)
    
    def test_get_price_by_block(self):
        """Test getting price by block number"""
        # Test with a block number that has an exact mapping
        price = self.oracle.get_price_by_block('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 15000000)
        self.assertEqual(price, 1380.25)  # Timestamp 1650695530 is closest to 1611532800
        
        # Test with a block number that requires interpolation
        price = self.oracle.get_price_by_block('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 14500000)
        self.assertEqual(price, 1380.25)  # Should get the closest timestamp's price
    
    def test_fast_price(self):
        """Test fast price method for ETH"""
        # Test with block 19302940 (should round to 19300000)
        price = self.oracle.fast_price(19302940)
        self.assertEqual(price, 1380.25)  # Timestamp 1717400000 is matched to closest price
        
        # Test with block 18039284 (should round to 18040000)
        price = self.oracle.fast_price(18039284)
        self.assertEqual(price, 1380.25)  # Timestamp 1694983820 is matched to closest price
    
    def test_missing_block_timestamps(self):
        """Test case when block timestamps file is missing"""
        # Save and delete block timestamps
        block_file = self.data_dir / 'eth_block_timestamps.csv'
        if block_file.exists():
            os.remove(block_file)
        
        # Create new oracle without block timestamps
        oracle_no_blocks = Oracle(data_dir=self.data_dir)
        
        # Should return None for block lookups
        self.assertIsNone(oracle_no_blocks.get_price_by_block('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 15000000))
        self.assertIsNone(oracle_no_blocks.fast_price(19302940))

if __name__ == '__main__':
    unittest.main() 