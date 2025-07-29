from azure.identity import DefaultAzureCredential
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.ingest import KustoStreamingIngestClient

from .kusto_config import KustoConfig


class KustoConnection:
    config: KustoConfig
    _client: KustoClient
    _ingestion_client: KustoStreamingIngestClient

    def __init__(self, config: KustoConfig):
        self.config = config
        self._client = self._create_client()
        self._ingestion_client = self._create_ingestion_client()

    def _create_client(self) -> KustoClient:
        # Try AzureCliCredential first (which we just refreshed with az login)
        # Fall back to DefaultAzureCredential if CLI credential fails
        credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)

        kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
            connection_string=self.config.query_service_uri, credential=credential
        )

        return KustoClient(kcsb)

    def _create_ingestion_client(self) -> KustoStreamingIngestClient:
        # Use the same credential approach as the query client
        credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
        kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
            connection_string=self.config.query_service_uri, credential=credential
        )
        return KustoStreamingIngestClient(kcsb)

    @property
    def client(self) -> KustoClient:
        return self._client

    @property
    def ingestion_client(self) -> KustoStreamingIngestClient:
        return self._ingestion_client
