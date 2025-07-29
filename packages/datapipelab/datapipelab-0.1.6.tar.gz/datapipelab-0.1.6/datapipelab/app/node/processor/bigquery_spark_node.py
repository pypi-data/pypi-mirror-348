from datapipelab.app.node.tnode import TNode
from datapipelab.logger import logger

class BigQuerySparkProcessorNode(TNode):
    def __init__(self, spark, tnode_config):
        super().__init__(spark=spark)
        self.sql_query = tnode_config['options']['query']
        self.node_name = tnode_config['name']
        self.credentials_path = tnode_config['options']['materialization_dataset'] # materializationDataset
        self.return_as_spark_df = tnode_config['options']['parent_project'] # parentProject

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
