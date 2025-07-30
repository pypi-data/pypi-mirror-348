# RTEdata

Python wrapper for [RTE API](https://data.rte-france.com/) requests. 

## 1. Usage

#### 1.1. Get RTE API credentials

You need to follow these first steps in order to setup your wrapper :  

* [create an account](https://data.rte-france.com/create_account) on the RTE platform
* [create an application](https://data.rte-france.com/group/guest/apps) associated to your account (the name and description of the app is not relevant)
* collect your app IDs (**ID Client** and **ID Secret**) available in your application dashboard

#### 1.2. Generate a data retrieval

To retrieve data using the wrapper, follow this pipeline :

```python
from rtedata import Client
client = Client(client_id="XXX", client_secret="XXX")
dfs = client.retrieve_data(start_date="2024-01-01 00:00:00", end_date="2024-01-02 23:59:00", data_type="actual_generations_per_unit", output_dir="./output")
```

where :
* **start_date** is the first date of the data retrieval (format *YYYY-MM-DD HH:MM:SS*)
* **end_date** is the last date of the data retrieval (format *YYYY-MM-DD HH:MM:SS*)
* **data_type** is the desired data to collect (a keyword list is given in the next section). It can be a single keyword *"XXX"* or a list of keyword separated by a comma *"XXX,YYY,ZZZ"*
* **output_dir** (*optionnal*): the output directory to store the results

The generic output format is a pandas dataframe / **.csv** file containing the data for all dates between **start_date** and **end_date**. It will generate one file per desired **data_type** and will store all of them in a **./results** folder with the generic name *"<data_type>_<start_date>_<end_date>.csv"*.

## 2. Available *data_type* options

It is possible to see the full options catalog using the client attribute **catalog** :

```python
from rtedata import Client
client = Client(client_id="XXX", client_secret="XXX")
client.catalog
```

The following table is an exhaustive list of all possible (currently handled) options for the **data_type** argument for the retrieval, and the description of the associated data :

| *data_type* | Request URL (Base) | Documentation |
|-------------------|-----|-----|
| `actual_generations_per_production_type` | *[Link](https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_production_type)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Actual+Generation/1.1)*|
| `actual_generations_per_unit` | *[Link](https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_unit)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Actual+Generation/1.1)*|
| `volumes_per_energy_type` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/volumes_per_energy_type)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `prices` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/prices)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `imbalance_data` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/imbalance_data)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `standard_rr_data` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/standard_rr_data)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `lead_times` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/lead_times)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `afrr_marginal_price` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/afrr_marginal_price)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `volumes_per_entity_price` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/volumes_per_entity_price)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `tso_offers` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/tso_offers)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `standard_afrr_data` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/standard_afrr_data)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `volumes_per_reasons` | *[Link](https://digital.iservices.rte-france.com/open_api/balancing_energy/v4/volumes_per_reasons)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*|
| `other_market_information` | *[Link](https://digital.iservices.rte-france.com/open_api/unavailability_additional_information/v6/other_market_information)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*|
| `transmission_network_unavailabilities` | *[Link](https://digital.iservices.rte-france.com/open_api/unavailability_additional_information/v6/transmission_network_unavailabilities)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*|
| `generation_unavailabilities_versions` | *[Link](https://digital.iservices.rte-france.com/open_api/unavailability_additional_information/v6/generation_unavailabilities_versions)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*|
| `transmission_network_unavailabilities_versions` | *[Link](https://digital.iservices.rte-france.com/open_api/unavailability_additional_information/v6/transmission_network_unavailabilities_versions)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*|
| `generation_unavailabilities` | *[Link](https://digital.iservices.rte-france.com/open_api/unavailability_additional_information/v6/generation_unavailabilities)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*|
| `other_market_information_versions` | *[Link](https://digital.iservices.rte-france.com/open_api/unavailability_additional_information/v6/other_market_information_versions)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*|
| `capacities_cpc` | *[Link](https://digital.iservices.rte-france.com/open_api/generation_installed_capacities/v1/capacities_cpc)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Generation+Installed+Capacities/1.1)*|
| `capacities_per_production_type` | *[Link](https://digital.iservices.rte-france.com/open_api/generation_installed_capacities/v1/capacities_per_production_type)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Generation+Installed+Capacities/1.1)*|
| `capacities_per_production_unit` | *[Link](https://digital.iservices.rte-france.com/open_api/generation_installed_capacities/v1/capacities_per_production_unit)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Generation+Installed+Capacities/1.1)*|

