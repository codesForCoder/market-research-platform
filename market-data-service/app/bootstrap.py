from app.brokers.dhan.dhan_market_feed_client import DhanMarketFeedClient
from app.brokers.dhan.dhan_market_feed_full_depth_client import DhanMarketFeedFullDepthClient
from app.brokers.dhan.dhan_option_chain_client import DhanOptionChainClient
from app.core.config import get_settings
from app.core.http_client import http_client

from app.brokers.dhan.instrument_downloader import InstrumentDownloader
from app.brokers.dhan.seed_csv_loader import SeedCsvLoader
from app.brokers.dhan.instrument_data_source import InstrumentDataSource
from app.brokers.dhan.instrument_mapper import DhanInstrumentMapper
from app.market_data.market_feed_manager import MarketFeedManager
from app.market_data.option_chain_manager import OptionChainManager
from app.market_data.option_chain_scheduler import OptionChainScheduler
from app.market_data.subscription_manager import SubscriptionManager

from app.repository.repository_builder import RepositoryBuilder
from app.repository.repository_manager import RepositoryManager
from app.scheduler.instrument_scheduler import InstrumentScheduler

from app.services.instrument_loader import InstrumentLoader


repository_manager = RepositoryManager()

mapper = DhanInstrumentMapper()

repository_builder = RepositoryBuilder()

downloader = InstrumentDownloader(http_client)

seed_loader = SeedCsvLoader()

data_source = InstrumentDataSource(
    downloader=downloader,
    seed_loader=seed_loader,
)

instrument_loader = InstrumentLoader(
    data_source=data_source,
    mapper=mapper,
    repository_builder=repository_builder,
    repository_manager=repository_manager,
)

instrument_scheduler = InstrumentScheduler(
    instrument_loader,
)


#Dhan support 5 clients - 3 allocated to 5 depth , 1 for 20 depth, 1 for 200 depth
market_feed_clients = []
for websocket_client_count in range(get_settings().DHAN_5_DEPTH_WEBSOCKET_ALLOCATION):
    market_feed_clients.append(DhanMarketFeedClient(get_settings().DHAN_CLIENT_ID, get_settings().DHAN_ACCESS_TOKEN))
market_feed_manager = MarketFeedManager(
    market_feed_clients
)
subscription_manager = SubscriptionManager(
    market_feed_clients
)

market_feed_clients_20 = []
for websocket_client_count in range(get_settings().DHAN_20_DEPTH_WEBSOCKET_ALLOCATION):
    market_feed_clients_20.append(DhanMarketFeedFullDepthClient(get_settings().DHAN_CLIENT_ID, get_settings().DHAN_ACCESS_TOKEN , 20))

market_feed_manager_20 = MarketFeedManager(
    market_feed_clients_20
)
subscription_manager_20 = SubscriptionManager(
    market_feed_clients_20
)

market_feed_clients_200 = []
for websocket_client_count in range(get_settings().DHAN_200_DEPTH_WEBSOCKET_ALLOCATION):
    market_feed_clients_200.append(DhanMarketFeedFullDepthClient(get_settings().DHAN_CLIENT_ID, get_settings().DHAN_ACCESS_TOKEN , 200))

market_feed_manager_200 = MarketFeedManager(
    market_feed_clients_200
)
subscription_manager_200 = SubscriptionManager(
    market_feed_clients_200
)

option_chain_manager = OptionChainManager()

option_chain_client = DhanOptionChainClient(get_settings().DHAN_CLIENT_ID, get_settings().DHAN_ACCESS_TOKEN)

option_chain_scheduler = OptionChainScheduler(
    option_chain_manager=option_chain_manager,
    option_chain_client=option_chain_client,
    polling_interval_seconds=get_settings().DHAN_OPTION_API_POLLING_INTERVAL
)
