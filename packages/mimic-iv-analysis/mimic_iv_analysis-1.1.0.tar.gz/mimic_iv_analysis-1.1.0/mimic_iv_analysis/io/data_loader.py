# Standard library imports
import os
import glob
import logging
import traceback
from pathlib import Path
from functools import lru_cache, cached_property
from typing import Dict, Optional, Tuple, List, Any, Union, Literal, Set
import warnings
import enum

# Data processing imports
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import dask.dataframe as dd
import humanize
from tqdm import tqdm
# Our modules
from mimic_iv_analysis.core.params import ( TableNamesHOSP,
											TableNamesICU,
											dtypes_all,
											parse_dates_all,
											pyarrow_dtypes_map,
											COLUMN_TYPES,
											DATETIME_COLUMNS,
											TABLE_CATEGORICAL_COLUMNS,
											convert_table_names_to_enum_class,
											DEFAULT_MIMIC_PATH,
											DEFAULT_NUM_SUBJECTS,
											SUBJECT_ID_COL,
											DEFAULT_STUDY_TABLES_LIST)


from mimic_iv_analysis.core.filtering import Filtering

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
	"""Handles scanning, loading, and providing info for MIMIC-IV data."""

	def __init__(self,
				mimic_path: Path = DEFAULT_MIMIC_PATH,
				study_tables_list: Optional[List[TableNamesHOSP | TableNamesICU]] = None):
		# MIMIC_IV v3.1 path
		self.mimic_path = mimic_path

		# Tables to load. Use list provided by user or default list
		self.study_table_list = study_tables_list or DEFAULT_STUDY_TABLES_LIST

		# Class variables
		self._all_subject_ids       : List[int]                = []
		self.tables_info_df          : Optional[pd.DataFrame]  = None
		self.tables_info_dict       : Optional[Dict[str, Any]] = None
		self.partial_subject_id_list: Optional[List[int]]      = None

	@lru_cache(maxsize=None)
	def scan_mimic_directory(self):
		"""Scans the MIMIC-IV directory structure and updates the tables_info_df and tables_info_dict attributes.

			tables_info_df is a DataFrame containing info:
				pd.DataFrame: DataFrame containing columns:
					- module      : The module name (hosp/icu)
					- table_name  : Name of the table
					- file_path   : Full path to the file
					- file_size   : Size of file in MB
					- display_name: Formatted display name with size
					- suffix      : File suffix (csv, csv.gz, parquet)
					- columns_list: List of columns in the table

			tables_info_dict is a dictionary containing info:
				Dict[str, Any]: Dictionary containing keys:
					- available_tables   : Dictionary of available tables
					- file_paths         : Dictionary of file paths
					- file_sizes         : Dictionary of file sizes
					- table_display_names: Dictionary of table display names
					- suffix             : Dictionary of file suffixes
					- columns_list       : Dictionary of column lists
				"""

		def _get_list_of_available_tables(module_path: Path) -> Dict[str, Path]:
			"""Lists unique table files from a module path."""

			POSSIBLE_FILE_TYPES = ['.parquet', '.csv', '.csv.gz']

			def _get_all_files() -> List[str]:
				filenames = []
				for suffix in POSSIBLE_FILE_TYPES:
					tables_path_list = glob.glob(os.path.join(module_path, f'*{suffix}'))
					if not tables_path_list:
						continue

					filenames.extend([os.path.basename(table_path).replace(suffix, '') for table_path in tables_path_list])

				return list(set(filenames))

			def _get_priority_file(table_name: str) -> Optional[Path]:
				# First priority is parquet
				if (module_path / f'{table_name}.parquet').exists():
					return module_path / f'{table_name}.parquet'

				# Second priority is csv
				if (module_path / f'{table_name}.csv').exists():
					return module_path / f'{table_name}.csv'

				# Third priority is csv.gz
				if (module_path / f'{table_name}.csv.gz').exists():
					return module_path / f'{table_name}.csv.gz'

				# If none exist, return None
				return None

			filenames = _get_all_files()

			return {table_name: _get_priority_file(table_name) for table_name in filenames}

		def _get_available_tables_info(available_tables_dict: Dict[str, Path], module: Literal['hosp', 'icu']):
			"""Extracts table information from a dictionary of table files."""

			def _get_file_size_in_bytes(file_path: Path) -> int:
				if file_path.suffix == '.parquet':
					return sum(f.stat().st_size for f in file_path.rglob('*') if f.is_file())
				return file_path.stat().st_size

			tables_info_dict['available_tables'][module] = []

			# Iterate through all tables in the module
			for table_name, file_path in available_tables_dict.items():

				if file_path is None or not file_path.exists():
					continue

				# Add to available tables
				tables_info_dict['available_tables'][module].append(table_name)

				# Store file path
				tables_info_dict['file_paths'][(module, table_name)] = file_path

				# Store file size
				tables_info_dict['file_sizes'][(module, table_name)] = _get_file_size_in_bytes(file_path)

				# Store display name
				tables_info_dict['table_display_names'][(module, table_name)] = (
					f"{table_name} {humanize.naturalsize(_get_file_size_in_bytes(file_path))}"
				)

				# Store file suffix
				suffix = file_path.suffix
				tables_info_dict['suffix'][(module, table_name)] = 'csv.gz' if suffix == '.gz' else suffix

				# Store columns
				if suffix == '.parquet':
					df = dd.read_parquet(file_path)
				else:
					df = pd.read_csv(file_path, nrows=1)
				tables_info_dict['columns_list'][(module, table_name)] = set(df.columns.tolist())

		def _get_info_as_dataframe() -> pd.DataFrame:
			table_info = []
			for module in tables_info_dict['available_tables']:
				for table_name in tables_info_dict['available_tables'][module]:

					file_path = tables_info_dict['file_paths'][(module, table_name)]

					table_info.append({
						'module'      : module,
						'table_name'  : table_name,
						'file_path'   : file_path,
						'file_size'   : tables_info_dict['file_sizes'][(module, table_name)],
						'display_name': tables_info_dict['table_display_names'][(module, table_name)],
						'suffix'      : tables_info_dict['suffix'][(module, table_name)],
						'columns_list': tables_info_dict['columns_list'][(module, table_name)]
					})

			# Convert to DataFrame
			dataset_info_df = pd.DataFrame(table_info)

			# Add mimic path as an attribute
			dataset_info_df.attrs['mimic_path'] = self.mimic_path

			return dataset_info_df

		# Initialize dataset info
		tables_info_dict = {
			'available_tables'   : {},
			'file_paths'         : {},
			'file_sizes'         : {},
			'table_display_names': {},
			'suffix'             : {},
			'columns_list'       : {},
		}

		# If the mimic path does not exist, return an empty DataFrame
		if not self.mimic_path.exists():
			self.tables_info_df = pd.DataFrame(columns=tables_info_dict.keys())
			return None, None

		# Iterate through modules
		modules = ['hosp', 'icu']
		for module in modules:

			# Get module path
			module_path: Path = self.mimic_path / module

			# if the module does not exist, skip it
			if not module_path.exists():
				continue

			# Get available tables:
			available_tables_dict = _get_list_of_available_tables(module_path)

			# If no tables found, skip this module
			if not available_tables_dict:
				continue

			# Get available tables info
			_get_available_tables_info(available_tables_dict, module)

		# Convert to DataFrame
		self.tables_info_df = _get_info_as_dataframe()
		self.tables_info_dict = tables_info_dict

	@property
	def study_tables_info(self) -> pd.DataFrame:
		"""Returns a DataFrame containing info for tables in the study."""

		if self.tables_info_df is None:
			self.scan_mimic_directory()

		# Get tables in the study
		study_tables = [table.value for table in self.study_table_list]

		return self.tables_info_df[self.tables_info_df.table_name.isin(study_tables)]

	@property
	def _list_of_tables_w_subject_id_column(self) -> List[TableNamesHOSP | TableNamesICU]:
		"""Returns a list of tables that have subject_id column."""
		tables_list = self.study_tables_info[
			self.study_tables_info.columns_list.apply(lambda x: 'subject_id' in x)
		].table_name.tolist()

		return [convert_table_names_to_enum_class(name=table_name, module='hosp')
				for table_name in tables_list]

	def _get_column_dtype(self, file_path: Optional[Path] = None, columns_list: Optional[List[str]] = None) -> Tuple[Dict[str, str], List[str]]:
		"""Determine the best dtype for a column based on its name and table."""

		if file_path is None and columns_list is None:
			raise ValueError("Either file_path or columns_list must be provided.")


		if file_path is not None:
			columns_list = pd.read_csv(file_path, nrows=1).columns.tolist()

		dtypes      = {col: dtype for col, dtype in COLUMN_TYPES.items() if col in columns_list}
		parse_dates = [col for col in DATETIME_COLUMNS if col in columns_list]

		return dtypes, parse_dates

	def load_csv_table_with_correct_column_datatypes(self, file_path: Path, use_dask: bool = True):
		# Check if file exists
		if not os.path.exists(file_path):
			raise FileNotFoundError(f"CSV file not found: {file_path}")

		if file_path.suffix not in ['.csv', '.gz', '.csv.gz']:
			logging.warning(f"File {file_path} is not a CSV file. Skipping.")
			return pd.DataFrame()

		# First read a small sample to get column names without type conversion
		dtypes, parse_dates = self._get_column_dtype(file_path=file_path)

		# Read with either dask or pandas based on user choice
		if use_dask:
			df = dd.read_csv(
				urlpath        = file_path,
				dtype          = dtypes,
				parse_dates    = parse_dates if parse_dates else None,
				assume_missing = True,
				blocksize      = None if file_path.suffix == '.gz' else '200MB'
			)
		else:
			df = pd.read_csv(
				filepath_or_buffer = file_path,
				dtype       = dtypes,
				parse_dates = parse_dates if parse_dates else None
			)

		return df

	def _get_file_path(self, table_name: TableNamesHOSP | TableNamesICU) -> Path:
		"""Get the file path for a table."""
		return Path(self.tables_info_df[
			(self.tables_info_df.table_name == table_name.value) &
			(self.tables_info_df.module == table_name.module)
		]['file_path'].iloc[0])

	@lru_cache(maxsize=None)
	def _load_unique_subject_ids_for_table(self, table_name: TableNamesHOSP | TableNamesICU = TableNamesHOSP.ADMISSIONS ) -> List[int]:
		"""
		Load unique subject IDs from the table_name.

		Retrieves all unique subject IDs from the table_name and stores them
		in the _subject_ids_list attribute. If the table_name cannot be found,
		an empty list will be stored instead.
		"""
		logging.info(f"Loading subject IDs from {table_name.value} table (this will be cached)")

		# Scan directory if not already done
		if self.tables_info_df is None:
			self.scan_mimic_directory()

		self._all_subject_ids = self.load_table( table_name=table_name, partial_loading=False )['subject_id'].unique().compute().tolist()

		return self._all_subject_ids

	@cached_property
	def all_subject_ids(self) -> List[int]:
		"""Returns a list of unique subject_ids found in the admission table."""
		# TODO: I changed this to get the intersection of all subject IDs found in the tables that have subject_id column. but now, it returns empty. why? (could i do the filtering after I merged all the tables?)
		def _load_unique_subject_id_common_between_all_tables():
			subject_ids = []
			for table_name in self._list_of_tables_w_subject_id_column:
				subject_ids.append(set(self.load_table(table_name=table_name, partial_loading=False)['subject_id'].unique().compute().tolist()))

			# get the intersection of all subject IDs
			self._all_subject_ids = list(set.intersection(*subject_ids))


		# Load subject IDs if not already loaded or if the list is empty
		if not self._all_subject_ids:
			_ = self._load_unique_subject_ids_for_table()

			# self._load_unique_subject_id_common_between_all_tables()


		return self._all_subject_ids

	def get_partial_subject_id_list_for_partial_loading(self, num_subjects: int = DEFAULT_NUM_SUBJECTS, random_selection: bool = False ) -> List[int]:
		"""
		Returns a subset of subject IDs for sampling.

		Args:
			num_subjects: Number of subject IDs to return. If 0 or negative, returns None.
			random_selection: If True, randomly selects the subject IDs. Otherwise, takes the first N.

		Returns:
			List of subject IDs for sampling, or empty list if appropriate.
		"""
		# If no subject IDs or num_subjects is non-positive, return an empty list
		if not self.all_subject_ids or num_subjects <= 0:
			return []

		# If num_subjects is greater than the number of available subject IDs, return all subject IDs
		if num_subjects > len(self.all_subject_ids):
			return self.all_subject_ids

		# Randomly select subject IDs if random_selection is True
		if random_selection:
			self.partial_subject_id_list = np.random.choice(
				a       = self.all_subject_ids,
				size    = num_subjects,
				replace = False
			).tolist()
		else:
			# Otherwise, return the first N subject IDs
			self.partial_subject_id_list = self.all_subject_ids[:num_subjects]

		return self.partial_subject_id_list

	def load_all_study_tables(self,
							partial_loading  : bool = False,
							num_subjects     : int  = DEFAULT_NUM_SUBJECTS,
							random_selection : bool = False,
							use_dask         : bool = True,
							subject_ids      : Optional[List[int]] = None,
							) -> Dict[str, pd.DataFrame | dd.DataFrame]:
		"""
		Load all tables in the study.

		Args            :
		partial_loading : Whether to load only a subset of subjects
		num_subjects    : Number of subjects to load if partial_loading is True
		random_selection: Whether to randomly select subjects
		subject_ids     : Optional list of subject IDs to load
		use_dask        : Whether to use Dask for loading

		Returns:
			Dictionary mapping table names to DataFrames
		"""
		# Get subject IDs for partial loading
		if partial_loading and (subject_ids is None):
			subject_ids = self.get_partial_subject_id_list_for_partial_loading(
				num_subjects=num_subjects,
				random_selection=random_selection
			)

		tables_dict = {}
		for _, row in self.study_tables_info.iterrows():
			table_name = convert_table_names_to_enum_class(name=row.table_name, module=row.module)

			tables_dict[table_name.value] = self.load_table(
				table_name=table_name,
				partial_loading=partial_loading,
				subject_ids=subject_ids,
				use_dask=use_dask
			)

		return tables_dict

	def load_table(self,
				table_name     : TableNamesHOSP | TableNamesICU,
				partial_loading: bool = False,
				subject_ids    : Optional[List[int]] = None,
				use_dask       : bool = True
				) -> pd.DataFrame | dd.DataFrame:
		"""
		Load a single table.

		Args:
			table_name     : The table to load
			partial_loading: Whether to load only a subset of subjects
			subject_ids    : Optional list of subject IDs to load
			use_dask       : Whether to use Dask for loading

		Returns:
			The loaded DataFrame
		"""
		def _load_table_full() -> pd.DataFrame | dd.DataFrame:
			file_path = self._get_file_path(table_name=table_name)

			# For parquet files, respect the use_dask flag
			if file_path.suffix == '.parquet':
				if use_dask:
					return dd.read_parquet(file_path)
				else:
					return pd.read_parquet(file_path)

			return self.load_csv_table_with_correct_column_datatypes(file_path, use_dask=use_dask)

		def _partial_loading(df):
			if subject_ids is None:
				raise ValueError("partial_loading is True but subject_ids is None")

			if 'subject_id' not in df.columns:
				logging.info(f"Table {table_name.value} does not have a subject_id column. "
							f"Partial loading is not possible. Skipping partial loading.")
				return df

			logging.info(f"Filtering {table_name.value} by subject_id for {len(subject_ids)} subjects.")

			# Convert subject_ids to a set for faster lookups
			subject_ids_set = set(subject_ids)

			# Use map_partitions for Dask DataFrame or direct isin for pandas
			if isinstance(df, dd.DataFrame):
				return df.map_partitions(lambda part: part[part['subject_id'].isin(subject_ids_set)])

			return df[df['subject_id'].isin(subject_ids_set)]

		def _get_n_rows(df):
			n_rows = df.size.compute() / len(df.columns) if isinstance(df, dd.DataFrame) else df.shape[0]
			return humanize.intcomma(int(n_rows))

		logging.info(f"Loading ----- {table_name.value} ----- table.")

		# Load table
		df = _load_table_full()
		logging.info(f"Loading full table: {_get_n_rows(df)} rows.")

		# Apply filtering
		df = Filtering(df=df, table_name=table_name).render()
		logging.info(f"Applied filters: {_get_n_rows(df)} rows.")

		# Apply partial loading if requested
		if partial_loading:
			df = _partial_loading(df)
			logging.info(f"Applied partial loading: {_get_n_rows(df)} rows.")

		return df

	def load_with_pandas_chunking(self,
									file_path         : Path,
									target_subject_ids: List[int],
									max_chunks        : Optional[int] = None,
									read_params       : Optional[Dict[str, Any]] = None
								) -> Tuple[pd.DataFrame, int]:
		"""
		Loads a large file by filtering by subject_ids using pandas chunking.

		Args:
			file_path: Path to the file to load
			target_subject_ids: List of subject IDs to filter by
			max_chunks: Maximum number of chunks to read
			read_params: Additional parameters for pd.read_csv

		Returns:
			Tuple of (filtered DataFrame, number of rows loaded)
		"""
		logging.info(f"Using Pandas chunking to filter by subject_id for {os.path.basename(file_path)}.")

		# Initialize variables
		chunks_for_target_ids = []
		processed_chunks = 0

		# Set default read parameters if not provided
		if read_params is None:
			read_params = {}

		read_params['dtype'], read_params['parse_dates'] = self._get_column_dtype(file_path=file_path)


		# Read the file in chunks
		with pd.read_csv(file_path, chunksize=100000, **read_params) as reader:

			# Iterate through chunks
			for chunk in reader:

				# Increment processed chunks counter
				processed_chunks += 1

				# Filter chunk by target_subject_ids
				filtered_chunk = chunk[chunk[SUBJECT_ID_COL].isin(target_subject_ids)]

				# Add to chunks if not empty
				if not filtered_chunk.empty:
					chunks_for_target_ids.append(filtered_chunk)

				# Check if we've reached max chunks
				if max_chunks is not None and max_chunks != -1 and processed_chunks >= max_chunks:
					logging.info(f"Reached max_chunks ({max_chunks}) during subject_id filtering for {os.path.basename(file_path)}.")
					break

			# Combine filtered chunks into final DataFrame
			if chunks_for_target_ids:
				df_result = pd.concat(chunks_for_target_ids, ignore_index=True)
			else:
				# Empty df with correct columns
				df_result = pd.DataFrame(columns=pd.read_csv(file_path, nrows=0).columns)

			# Calculate total rows loaded
			total_rows_loaded = len(df_result)

			# Log the result
			logging.info(f"Loaded {total_rows_loaded} rows for {len(target_subject_ids)} subjects from {os.path.basename(file_path)} using Pandas chunking.")

		return df_result, total_rows_loaded

	def load_merged_tables(self,
						partial_loading : bool = False,
						num_subjects    : int  = DEFAULT_NUM_SUBJECTS,
						random_selection: bool = False,
						use_dask        : bool = True,
						tables_dict     : Optional[Dict[str, pd.DataFrame | dd.DataFrame]] = None
						) -> Dict[str, pd.DataFrame | dd.DataFrame]:
		"""
		Load and merge tables.

		Args:
			partial_loading: Whether to load only a subset of subjects
			num_subjects: Number of subjects to load if partial_loading is True
			random_selection: Whether to randomly select subjects
			use_dask: Whether to use Dask for loading
			tables_dict: Optional dictionary of pre-loaded tables

		Returns:
			Dictionary of merged tables
		"""
		if tables_dict is None:
			tables_dict = self.load_all_study_tables(
				partial_loading  = partial_loading,
				num_subjects     = num_subjects,
				random_selection = random_selection,
				use_dask         = use_dask
			)

		# Get tables
		patients_df      = tables_dict[TableNamesHOSP.PATIENTS.value]
		admissions_df    = tables_dict[TableNamesHOSP.ADMISSIONS.value]
		diagnoses_icd_df = tables_dict[TableNamesHOSP.DIAGNOSES_ICD.value]
		d_icd_diagnoses_df = tables_dict[TableNamesHOSP.D_ICD_DIAGNOSES.value]
		poe_df             = tables_dict[TableNamesHOSP.POE.value]
		poe_detail_df      = tables_dict[TableNamesHOSP.POE_DETAIL.value]

		# Merge tables
		df12 = patients_df.merge(admissions_df, on='subject_id', how='inner')

		if TableNamesHOSP.TRANSFERS.value in tables_dict:
			transfers_df = tables_dict[TableNamesHOSP.TRANSFERS.value]
			df123 = df12.merge(transfers_df, on=['subject_id', 'hadm_id'], how='inner')
		else:
			df123 = df12

		diagnoses_merged = diagnoses_icd_df.merge(d_icd_diagnoses_df, on=['icd_code', 'icd_version'], how='inner')
		merged_wo_poe    = df123.merge(diagnoses_merged, on=['subject_id', 'hadm_id'], how='inner')

		# The reason for 'left' is that we want to keep all the rows from poe table.
		# The poe_detail table for unknown reasons, has fewer rows than poe table.
		poe_and_details   = poe_df.merge(poe_detail_df, on=['poe_id', 'poe_seq', 'subject_id'], how='left')
		merged_full_study = merged_wo_poe.merge(poe_and_details, on=['subject_id', 'hadm_id'], how='inner')

		return {
			'merged_wo_poe'    : merged_wo_poe,
			'merged_full_study': merged_full_study,
			'poe_and_details'  : poe_and_details
		}


class ExampleDataLoader:
	"""ExampleDataLoader class for loading example data."""

	def __init__(self, partial_loading: bool = False, num_subjects: int = 100, random_selection: bool = False, use_dask: bool = True):
		self.data_loader = DataLoader()
		self.data_loader.scan_mimic_directory()

		if partial_loading:
			self.tables_dict = self.data_loader.load_all_study_tables(
				partial_loading  = True,
				num_subjects     = num_subjects,
				random_selection = random_selection,
				use_dask         = use_dask
			)
		else:
			self.tables_dict = self.data_loader.load_all_study_tables(partial_loading=False, use_dask=use_dask)

		with warnings.catch_warnings():
			warnings.simplefilter("ignore")

	def counter(self):
		"""Print row and subject ID counts for each table."""

		def get_nrows(table_name):
			df = self.tables_dict[table_name.value]
			return humanize.intcomma(df.shape[0].compute() if isinstance(df, dd.DataFrame) else df.shape[0])

		def get_nsubject_ids(table_name):
			df = self.tables_dict[table_name.value]
			if 'subject_id' not in df.columns:
				return "N/A"
			# TODO: if returns errors, use df.subject_id.unique().shape[0].compute() instead
			return humanize.intcomma(
				df.subject_id.nunique().compute() if isinstance(df, dd.DataFrame)
				else df.subject_id.nunique()
			)

		# Format the output in a tabular format
		print(f"{'Table':<15} | {'Rows':<10} | {'Subject IDs':<10}")
		print(f"{'-'*15} | {'-'*10} | {'-'*10}")
		print(f"{'patients':<15} | {get_nrows(TableNamesHOSP.PATIENTS):<10} | {get_nsubject_ids(TableNamesHOSP.PATIENTS):<10}")
		print(f"{'admissions':<15} | {get_nrows(TableNamesHOSP.ADMISSIONS):<10} | {get_nsubject_ids(TableNamesHOSP.ADMISSIONS):<10}")
		print(f"{'diagnoses_icd':<15} | {get_nrows(TableNamesHOSP.DIAGNOSES_ICD):<10} | {get_nsubject_ids(TableNamesHOSP.DIAGNOSES_ICD):<10}")
		print(f"{'poe':<15} | {get_nrows(TableNamesHOSP.POE):<10} | {get_nsubject_ids(TableNamesHOSP.POE):<10}")
		print(f"{'poe_detail':<15} | {get_nrows(TableNamesHOSP.POE_DETAIL):<10} | {get_nsubject_ids(TableNamesHOSP.POE_DETAIL):<10}")

	def study_table_info(self):
		"""Get info about study tables."""
		return self.data_loader.study_tables_info

	def merge_two_tables(self, table1: TableNamesHOSP | TableNamesICU, table2: TableNamesHOSP | TableNamesICU, on: Tuple[str], how: Literal['inner', 'left', 'right', 'outer'] = 'inner'):
		"""Merge two tables."""
		df1 = self.tables_dict[table1.value]
		df2 = self.tables_dict[table2.value]

		# Ensure compatible types for merge columns
		for col in on:
			if col in df1.columns and col in df2.columns:

				# Convert to same type in both dataframes
				if col.endswith('_id') and col not in ['poe_id', 'emar_id', 'pharmacy_id']:
					df1[col] = df1[col].astype('int64')
					df2[col] = df2[col].astype('int64')

				elif col in ['icd_code', 'icd_version']:
					df1[col] = df1[col].astype('string')
					df2[col] = df2[col].astype('string')

				elif col in ['poe_id', 'emar_id', 'pharmacy_id'] or col.endswith('provider_id'):
					df1[col] = df1[col].astype('string')
					df2[col] = df2[col].astype('string')

		return df1.merge(df2, on=on, how=how)

	def save_as_parquet(self, table_name: TableNamesHOSP | TableNamesICU):
		"""Save a table as Parquet."""
		ParquetConverter(data_loader=self.data_loader).save_as_parquet(table_name=table_name)

	def n_rows_after_merge(self):
		"""Print row counts after merges."""
		patients_df        = self.tables_dict[TableNamesHOSP.PATIENTS.value]
		admissions_df      = self.tables_dict[TableNamesHOSP.ADMISSIONS.value]
		diagnoses_icd_df   = self.tables_dict[TableNamesHOSP.DIAGNOSES_ICD.value]
		poe_df             = self.tables_dict[TableNamesHOSP.POE.value]
		d_icd_diagnoses_df = self.tables_dict[TableNamesHOSP.D_ICD_DIAGNOSES.value]
		poe_detail_df      = self.tables_dict[TableNamesHOSP.POE_DETAIL.value]

		# Ensure compatible types
		patients_df        = self.data_loader.ensure_compatible_types(patients_df, ['subject_id'])
		admissions_df      = self.data_loader.ensure_compatible_types(admissions_df, ['subject_id', 'hadm_id'])
		diagnoses_icd_df   = self.data_loader.ensure_compatible_types(diagnoses_icd_df, ['subject_id', 'hadm_id', 'icd_code', 'icd_version'])
		d_icd_diagnoses_df = self.data_loader.ensure_compatible_types(d_icd_diagnoses_df, ['icd_code', 'icd_version'])
		poe_df             = self.data_loader.ensure_compatible_types(poe_df, ['subject_id', 'hadm_id', 'poe_id', 'poe_seq'])
		poe_detail_df      = self.data_loader.ensure_compatible_types(poe_detail_df, ['subject_id', 'poe_id', 'poe_seq'])

		df12              = patients_df.merge(admissions_df, on='subject_id', how='inner')
		df34              = diagnoses_icd_df.merge(d_icd_diagnoses_df, on=('icd_code', 'icd_version'), how='inner')
		poe_and_details   = poe_df.merge(poe_detail_df, on=('poe_id', 'poe_seq', 'subject_id'), how='left')
		merged_wo_poe     = df12.merge(df34, on=('subject_id', 'hadm_id'), how='inner')
		merged_full_study = merged_wo_poe.merge(poe_and_details, on=('subject_id', 'hadm_id'), how='inner')

		def get_count(df):
			return df.shape[0].compute() if isinstance(df, dd.DataFrame) else df.shape[0]

		print(f"{'DataFrame':<15} {'Count':<10} {'DataFrame':<15} {'Count':<10} {'DataFrame':<15} {'Count':<10}")
		print("-" * 70)
		print(f"{'df12':<15} {get_count(df12):<10} {'patients':<15} {get_count(patients_df):<10} {'admissions':<15} {get_count(admissions_df):<10}")
		print(f"{'df34':<15} {get_count(df34):<10} {'diagnoses_icd':<15} {get_count(diagnoses_icd_df):<10} {'d_icd_diagnoses':<15} {get_count(d_icd_diagnoses_df):<10}")
		print(f"{'poe_and_details':<15} {get_count(poe_and_details):<10} {'poe':<15} {get_count(poe_df):<10} {'poe_detail':<15} {get_count(poe_detail_df):<10}")
		print(f"{'merged_wo_poe':<15} {get_count(merged_wo_poe):<10} {'df34':<15} {get_count(df34):<10} {'df12':<15} {get_count(df12):<10}")
		print(f"{'merged_full_study':<15} {get_count(merged_full_study):<10} {'poe_and_details':<15} {get_count(poe_and_details):<10} {'merged_wo_poe':<15} {get_count(merged_wo_poe):<10}")

	def load_table(self, table_name: TableNamesHOSP | TableNamesICU):
		"""Load a single table."""
		return self.tables_dict[table_name.value]

	def load_all_study_tables(self):
		"""Load all study tables."""
		return self.tables_dict

	def load_merged_tables(self):
		"""Load merged tables."""
		return self.data_loader.load_merged_tables(tables_dict=self.tables_dict)


class ParquetConverter:
	"""Handles conversion of CSV/CSV.GZ files to Parquet format with appropriate schemas."""

	def __init__(self, data_loader: DataLoader):
		self.data_loader = data_loader

	def _get_csv_file_path(self, table_name: TableNamesHOSP | TableNamesICU) -> Tuple[Path, str]:
		"""
		Gets the CSV file path for a table.

		Args:
			table_name: The table to get the file path for

		Returns:
			Tuple of (file path, suffix)
		"""
		def _fix_source_csv_path(source_path: Path) -> Tuple[Path, str]:
			"""Fixes the source csv path if it is a parquet file."""

			if source_path.name.endswith('.parquet'):

				csv_path = source_path.parent / source_path.name.replace('.parquet', '.csv')
				gz_path = source_path.parent / source_path.name.replace('.parquet', '.csv.gz')

				if csv_path.exists():
					return csv_path, '.csv'

				if gz_path.exists():
					return gz_path, '.csv.gz'

				raise ValueError(f"Cannot find csv or csv.gz file for {source_path}")

			suffix = '.csv.gz' if source_path.name.endswith('.gz') else '.csv'

			return source_path, suffix

		if self.data_loader.tables_info_df is None:
			self.data_loader.scan_mimic_directory()


		source_path = Path(self.data_loader.tables_info_df[(self.data_loader.tables_info_df.table_name == table_name.value)]['file_path'].values[0])

		return _fix_source_csv_path(source_path)

	def _create_table_schema(self, df: pd.DataFrame | dd.DataFrame) -> pa.Schema:
		""" Create a PyArrow schema for a table based on column types. """

		column_names = df.columns.tolist()

		dtypes, _ = self._get_column_dtype(columns_list=column_names)

		# Create fields
		fields = [pa.field(col, pyarrow_dtypes_map.get(dtypes[col])) for col in column_names]

		# Create and return schema
		return pa.schema(fields)

	def save_as_parquet(self, table_name: TableNamesHOSP | TableNamesICU, df: Optional[pd.DataFrame | dd.DataFrame] = None, target_parquet_path: Optional[Path] = None, use_dask: bool = True) -> None:
		"""
		Saves a DataFrame as a Parquet file.

		Args:
			table_name: Table name to save as parquet
			df: Optional DataFrame to save (if None, loads from source_path)
			target_parquet_path: Optional target path for the parquet file
			use_dask: Whether to use Dask for loading
		"""
		if df is None or target_parquet_path is None:

			# Get csv file path
			csv_file_path, suffix = self._get_csv_file_path(table_name)

			# Load the CSV file
			if df is None:
				df = self.data_loader.load_csv_table_with_correct_column_datatypes(file_path=csv_file_path, use_dask=use_dask)

			# Get parquet directory
			if target_parquet_path is None:
				target_parquet_path = csv_file_path.parent / csv_file_path.name.replace(suffix, '.parquet')

		# Create schema
		schema = self._create_table_schema(df)

		# Save to parquet
		if isinstance(df, dd.DataFrame):
			df.to_parquet(target_parquet_path, schema=schema, engine='pyarrow', compression='snappy')
		else:
			# For pandas DataFrame
			table = pa.Table.from_pandas(df, schema=schema)
			pq.write_table(table, target_parquet_path, compression='snappy')

	def save_all_tables_as_parquet(self, tables_list: Optional[List[TableNamesHOSP | TableNamesICU]] = None) -> None:
		"""
		Save all tables as Parquet files.

		Args:
			tables_list: List of table names to convert
		"""
		# If no tables list is provided, use the study table list
		if tables_list is None:
			tables_list = self.data_loader.study_table_list

		# Save tables as parquet
		for table_name in tqdm(tables_list, desc="Saving tables as parquet"):
			self.save_as_parquet(table_name=table_name)


if __name__ == '__main__':

	# TODO: check that everything works after all the changes.
	# Load partial data
	# examples_partial = ExampleDataLoader(partial_loading=True, num_subjects=10, random_selection=False)

	# Convert admissions table to Parquet
	converter = ParquetConverter(data_loader=DataLoader(mimic_path=DEFAULT_MIMIC_PATH))
	converter.save_as_parquet(table_name=TableNamesHOSP.ADMISSIONS, use_dask=True)

	# Convert all study tables to Parquet
	# converter.save_all_tables_as_parquet()

	# Load from Parquet and merge
	# data_loader = DataLoader()
	# merged_tables = data_loader.load_merged_tables(partial_loading=True, num_subjects=10)

	print('done')
