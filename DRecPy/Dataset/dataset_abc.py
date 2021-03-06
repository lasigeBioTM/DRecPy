from abc import abstractmethod, ABC
from copy import copy


class InteractionDatasetABC(ABC):
    def __init__(self, **kwds):
        self.verbose = kwds.get('verbose', True)
        self.has_internal_ids = False
        self.columns = None

    @abstractmethod
    def __len__(self):
        """Compute the number of rows of the present InteractionDataset.

        Returns:
            An integer that represents the number of rows of the current InteractionDataset.
        """
        pass

    @abstractmethod
    def select(self, query, copy=True):
        """Select rows from the InteractionDataset.

        Args:
            query: A string representing the query to be run. The query format should be: "column_name operator value",
                where extra conditions should be separated by a ','. E.g. "user == '123', interaction > 3.5".
            copy: A boolean indicating whether to create a new InteractionDataset where the rows that satisfy the
                provided query are put, or if the filtered rows should be removed from the current InteractionDataset
                (copy=False). Default: True.

        Returns:
            An instance of a InteractionDataset containing the rows selected by the provided query.
        """
        pass

    @abstractmethod
    def select_random_generator(self, query=None):
        """Provides a generator that yields dataset rows.

        Args:
            query: A string representing the query to be run before selecting random rows. The query format should be:
                "column_name operator value", where extra conditions should be separated by a ','. E.g. "user == '123',
                interaction > 3.5".

        Returns:
            A generator that yields dataset rows, where each row is represented as a dict.
        """
        pass

    @abstractmethod
    def null_interaction_pair_generator(self, interaction_threshold=None, seed=None):
        """Provides a generator that yields negative / null interaction pairs.

        Args:
            interaction_threshold: An optional integer that is used as the boundary interaction value between positive
                and negative interaction pairs. All values above or equal interaction_threshold are considered positive,
                and all values bellow are considered negative. If none is provided, positive interactions are the ones
                present on the dataset, and all the others are considered negative. Default: None.
            seed: An optional integer to be used as the seed value for the pseudo-random number generated used to sample
                null interaction pairs. Default: None.

        Returns:
            A generator that yields negative / null interaction pairs, that is, (user internal id, item internal id)
            tuples.
        """
        pass

    def select_one(self, query, columns=None, to_list=False):
        """Select the first resulting row for the provided query.

        Args:
            query: A string representing the query to be run. The query format should be: "column_name operator value",
                where extra conditions should be separated by a ','. E.g. "user == '123', interaction > 3.5".
            columns: A list with the column names to be kept on the resulting record. Default: all.
            to_list: A boolean indicating whether each data point should be returned as a dict or as a list.
                Default: False.
        Returns:

        """
        return next(self.select(query).values(columns=columns, to_list=to_list), None)

    @abstractmethod
    def select_user_interaction_vec(self, uid):
        """Compute the user interaction vector for the provided user internal id.

        Args:
            uid: The user internal id that references the user that should have its interaction vector computed.

        Returns:
            The interaction vector (a vector containing the interaction values of each item to the provided user, in
            order) of the provided uid.
        """
        pass

    @abstractmethod
    def select_item_interaction_vec(self, iid):
        """Compute the item interaction vector for the provided item internal id.

        Args:
            iid: The item internal id that references the item that should have its interaction vector computed.

        Returns:
            The interaction vector (a vector containing the interaction values of each user to the provided item, in
            order) of the provided iid.
        """
        pass

    def exists(self, query):
        """Compute if the provided query handles at least 1 value or not.

        Args:
            query: A string representing the query to be run. The query format should be: "column_name operator value",
                where extra conditions should be separated by a ','. E.g. "user == '123', interaction > 3.5".

        Returns:
            A boolean indicating if the query handles any results or not.
        """
        return False if self.select_one(query) is None else True

    @abstractmethod
    def unique(self, columns=None, copy=True):
        """Return a new InteractionDataset instance containing only the unique values on the provided column
        combination.

        Args:
            columns: The column combination to take into account when computing unique values. Default: all.
            copy: A boolean indicating whether a copy of the InteractionDataset should be made, or if it should be
                modified in-place. Default: True.

        Returns:
            A InteractionDataset instance containing the unique values on the provided column combination.
        """
        pass

    def count_unique(self, columns=None):
        """Count the number of unique values on the provided column combination.

        Args:
            columns: A list containing the columns to take into account. Default: all.

        Returns:
            The count of unique values present on the provided column combination.
        """
        return len(self.unique(columns))

    @abstractmethod
    def max(self, column=None):
        """Computes the maximum value for the provided column.

        Args:
            column: The name of the column for which the maximum should be computed.

        Returns:
            The maximum value present on the whole dataset, for the provided column name.
        """
        pass

    @abstractmethod
    def min(self, column=None):
        """Computes the minimum value for the provided column.

        Args:
            column: The name of the column for which the minimum should be computed.

        Returns:
            The minimum value present on the whole dataset, for the provided column name.
        """
        pass

    @abstractmethod
    def values(self, columns=None, to_list=False):
        """Provides a generator that yields all the records present in the dataset.

        Args:
            columns: The list of columns that should be returned for each data point.  Default: all.
            to_list: A boolean indicating whether each data point should be returned as a dict or as a list.
                Default: False.

        Returns:
            A generator that yields records present in the dataset.
        """
        pass

    def values_list(self, columns=None, to_list=False):
        """Provides list with all the records present in the dataset.

        Args:
            columns: The list of columns that should be returned for each data point. Default: None (show all).
            to_list: A boolean indicating whether each data point should be returned as a dict or as a list.
                Default: False.

        Returns:
            A list containing all records present in the dataset.
        """
        return [record for record in self.values(columns=columns, to_list=to_list)]

    @abstractmethod
    def drop(self, record_ids, copy=True, keep=False):
        """Remove (or keep) the provided list of record ids from the current InteractionDataset instance.

        Args:
            record_ids: A list of integers representing record ids.
            copy: A boolean indicating whether to create a new InteractionDataset instance to remove (or keep) the
                provided list of record ids, or if the current InteractionDataset instance should be modified
                accordingly (copy=False). Default: True.
            keep: A boolean indicating whether the provided record ids should be kept or removed (keep=False).
                Default: False.

        Returns:
            An instance of the InteractionDataset with (or without) the filtered records.
        """
        pass

    @abstractmethod
    def assign_internal_ids(self):
        """Assigns user and item internal ids. Internal ids are integer consecutive identifiers that represent each
        user or item uniquely. Two new columns are created on this dataset instance: "uid" and "iid", for user internal
        id and item internal id, respectively.

        Returns:
            None.
        """
        pass

    @abstractmethod
    def remove_internal_ids(self):
        """Removes user and item internal ids.

        Returns:
            None.
        """
        pass

    @abstractmethod
    def user_to_uid(self, user):
        """Converts a given raw user id into its correspondent internal id. Raises exception if no internal ids are
        assigned.

        Args:
            user: The user raw id.

        Returns:
            An integer value representing the user internal id, or None if the raw user id provided does not exist.
        """
        pass

    @abstractmethod
    def uid_to_user(self, uid):
        """Converts a given internal user id into its correspondent raw id. Raises exception if no internal ids are
        assigned.

        Args:
            uid: The user internal id.

        Returns:
            An integer value representing the user raw id, or None if the internal user id provided does not exist.
        """
        pass

    @abstractmethod
    def item_to_iid(self, item):
        """Converts a given raw item id into its correspondent internal id. Raises exception if no internal ids are
        assigned.

        Args:
            item: The item raw id.

        Returns:
            An integer value representing the item internal id, or None if the raw item id provided does not exist.
        """
        pass

    @abstractmethod
    def iid_to_item(self, iid):
        """Converts a given internal item id into its correspondent raw id. Raises exception if no internal ids are
        assigned.

        Args:
            iid: The item internal id.

        Returns:
            An integer value representing the item raw id, or None if the internal item id provided does not exist.
        """
        pass

    @abstractmethod
    def apply(self, column, function):
        """Modifies the current dataset instance by applying a transformation to a specific column in every row.

        Args:
            column: A string that represents the name of the column that will be transformed.
            function: The function that will be used to map the current column value in each row to the new one.

        Returns:
            None.
        """
        pass

    @abstractmethod
    def save(self, path, columns=None, write_header=False):
        """Persists the current dataset instance in the provided path, as a csv file.
        Note that internal identifiers, such as the row id (rid), user internal id (uid) and item internal id (iid)
        are never persisted, since they're only useful during runtime.

        Args:
            path: A string that represents the path where the current dataset values will be persisted.
            columns: An optional list with the names of the columns that should be persisted. Default: all columns.
            write_header: A boolean indicating whether to write the csv header on the persisted file. Default: False.

        Returns:
            None.
        """
        pass

    @abstractmethod
    def copy(self):
        """Copies the current dataset instance into a new one.

        Returns:
            InteractionDataset instance with the same data values as the current one.
        """
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        if 'close' in dir(self):
            self.close()

    """ Private methods """
    def _validate_column(self, column):
        assert column is not None, 'No column was given.'
        assert type(column) is str, f'Unexpected column type "{type(column)}".'
        assert column in self.columns, f'Unexpected column "{column}".'

    def _handle_columns(self, columns):
        if columns is None: columns = copy(self.columns)
        if type(columns) is not list: columns = [columns]

        for c in columns:
            assert c in self.columns, f'Unexpected column "{c}".'

        return columns

    def _log(self, msg):
        if not self.verbose: return
        print(f'[{self.__class__.__name__}] {msg}')


