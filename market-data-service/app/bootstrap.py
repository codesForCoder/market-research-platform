from app.brokers.dhan.dhan_market_feed_client import DhanMarketFeedClient
from app.core.config import get_settings
from app.core.http_client import http_client

from app.brokers.dhan.instrument_downloader import InstrumentDownloader
from app.brokers.dhan.seed_csv_loader import SeedCsvLoader
from app.brokers.dhan.instrument_data_source import InstrumentDataSource
from app.brokers.dhan.instrument_mapper import DhanInstrumentMapper
from app.market_data.market_feed_manager import MarketFeedManager
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


#Dhan support 5 clients
market_feed_clients = []
for websocket_client_count in range(5):
    market_feed_clients.append(DhanMarketFeedClient(get_settings().DHAN_CLIENT_ID, get_settings().DHAN_ACCESS_TOKEN))
market_feed_manager = MarketFeedManager(
    market_feed_clients
)
subscription_manager = SubscriptionManager(
    market_feed_clients
)
