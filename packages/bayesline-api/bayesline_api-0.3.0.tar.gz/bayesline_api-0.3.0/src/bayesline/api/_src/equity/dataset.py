import abc


class DatasetApi(abc.ABC):

    @abc.abstractmethod
    def get_default_dataset_name(self) -> str:
        """
        Returns
        -------
        str
            The default dataset name that will be populated into settings if no
            dataset name is provided.
        """

    @abc.abstractmethod
    def get_dataset_names(self) -> list[str]:
        """
        Returns the names of all available datasets.

        Returns
        -------
        list[str]
            The names of all available datasets.
        """


class AsyncDatasetApi(abc.ABC):

    @abc.abstractmethod
    async def get_default_dataset_name(self) -> str:
        """
        Returns
        -------
        str
            The default dataset name that will be populated into settings if no
            dataset name is provided.
        """

    @abc.abstractmethod
    async def get_dataset_names(self) -> list[str]:
        """
        Returns the names of all available datasets.

        Returns
        -------
        list[str]
            The names of all available datasets.
        """
