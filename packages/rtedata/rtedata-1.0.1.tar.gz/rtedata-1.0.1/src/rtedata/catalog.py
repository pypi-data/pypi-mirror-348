from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Catalog:
    _structure: Dict[str, list[str]] = field(init=False, repr=False)

    def __post_init__(self):
      self.request_base_url = "https://digital.iservices.rte-france.com/open_api"
      self.docs_base_url = "https://data.rte-france.com/catalog/-/api/doc/user-guide"
      
      self._url_to_keys = {
        f"{self.request_base_url}/actual_generation/v1/" : ["actual_generations_per_production_type", "actual_generations_per_unit"],
        f"{self.request_base_url}/balancing_energy/v4/" : ["volumes_per_energy_type", "prices", "imbalance_data", "standard_rr_data", "lead_times", "afrr_marginal_price", "volumes_per_entity_price", "tso_offers", "standard_afrr_data", "volumes_per_reasons"],
        f"{self.request_base_url}/unavailability_additional_information/v6/" : ["other_market_information", "transmission_network_unavailabilities", "generation_unavailabilities_versions", "transmission_network_unavailabilities_versions", "generation_unavailabilities", "other_market_information_versions"],
        f"{self.request_base_url}/generation_installed_capacities/v1/" : ["capacities_cpc", "capacities_per_production_type", "capacities_per_production_unit"]
         }
      
      self._url_to_docs = {
          f"{self.request_base_url}/actual_generation/v1/" : f"{self.docs_base_url}/Actual+Generation/1.1",
          f"{self.request_base_url}/balancing_energy/v4/" : f"{self.docs_base_url}/Balancing+Energy/4.0",
          f"{self.request_base_url}/unavailability_additional_information/v6/" : f"{self.docs_base_url}/Unavailability+Additional+Information/6.0",
          f"{self.request_base_url}/generation_installed_capacities/v1/" : f"{self.docs_base_url}/Generation+Installed+Capacities/1.1"  
      }
      
      self._requests = {
          key : {"url": f"{prefix}{key}", "docs": self._url_to_docs.get(prefix)}
            for prefix, keys in self._url_to_keys.items()
            for key in keys
        }

    @property
    def keys(self) -> str:
        return list(self._requests.keys())
    
    def get_key_content(self, key: str) -> tuple[str, str]:
        key_content = self._requests.get(key, None)
        if key_content is None:
            raise KeyError(f"Request key '{key}' not in requests catalog")
        url = key_content.get("url")
        docs = key_content.get("docs", None)
        return url, docs
      
    def to_markdown(self) -> str:
        md = []
        md.append("| *data_type* | Request URL (Base) | Documentation |")
        md.append("|-------------------|-----|-----|")
        for key in self._requests:
            url, docs = self.get_key_content(key)
            docs = docs if docs is not None else "X"
            md.append(f"| `{key}` | *[Link]({url})* | *[Link]({docs})*|")
        return "".join(md)

    def __repr__(self):
        _repr = "rtedata Catalog : \n"
        for i, key in enumerate(self._requests):
                url, docs = self.get_key_content(key)
                _repr += f"{i} - {key} : \n"
                _repr += f"~> request base url : {url} \n"
                if docs is not None:
                    _repr += f"~> docs url : {docs} \n"
        return _repr
        
