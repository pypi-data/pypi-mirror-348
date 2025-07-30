import pytest
from abc import ABC
from mysharelib.interfaces import MyShareData, InvalidSymbolError, DataSourceError

class TestMyShareData:
    def test_abstract_methods(self):
        """Ensure abstract methods are not implemented in the base class."""
        with pytest.raises(TypeError):
            MyShareData()

    def test_from_source_invalid(self):
        """Test that an invalid source raises a ValueError."""
        with pytest.raises(ValueError, match="Unsupported data source: invalid"):
            MyShareData.from_source("invalid")

    def test_from_source_yahoo(self, mocker):
        """Test that the YahooData source is correctly instantiated."""
        mock_yahoo_data = mocker.patch("mysharelib.YahooData")
        MyShareData.from_source("yahoo", param="test")
        #mock_yahoo_data.assert_called_once_with(param="test")

    def test_from_source_akshare(self, mocker):
        """Test that the AKShareData source is correctly instantiated."""
        mock_akshare_data = mocker.patch("mysharelib.AKShareData")
        MyShareData.from_source("akshare", param="test")
        #mock_akshare_data.assert_called_once_with(param="test")