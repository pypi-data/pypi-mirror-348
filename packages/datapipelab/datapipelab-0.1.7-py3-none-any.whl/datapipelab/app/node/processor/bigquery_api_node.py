from datapipelab.app.node.tnode import TNode
from datapipelab.logger import logger

class BigQueryAPIProcessorNode(TNode):
    def __init__(self, spark, tnode_config):
        from google.cloud import bigquery
        from google.oauth2 import service_account
        super().__init__(spark=spark)
        self.sql_query = tnode_config['options']['query']
        self.node_name = tnode_config['name']
        self.credentials_path = tnode_config['options']['credentials_path']
        self.return_as_spark_df = tnode_config['options']['return_as_spark_df']
        self.project_name = tnode_config['options']['project_name']

    def __sql_query(self, sql_query):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        client = bigquery.Client(credentials=credentials, project=self.project_name)

        # run the job
        query_job = client.query(sql_query)

        results = query_job.result()
        rows = [dict(row) for row in results]
        if self.return_as_spark_df:
            self.node = self.spark.createDataFrame(rows)
        else:
            self.node = None
        logger.info(rows)

    def _process(self):
        self.__sql_query(self.sql_query)
        self._createOrReplaceTempView()
        return self.node
