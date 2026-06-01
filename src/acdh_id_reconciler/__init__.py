import os
from typing import Any, Mapping

import requests
from AcdhArcheAssets.uri_norm_rules import get_norm_id

from .utils import normalize_wikidata_id

USER_AGENT = "acdh-id-reconciler (https://www.oeaw.ac.at/acdh/acdh-ch-home)"
WIKIAPI_BASE = "https://www.wikidata.org/w/api.php"
WIKIAPI_URL = (
    f"{WIKIAPI_BASE}?action=wbgetentities&format=json&props=sitelinks/urls&ids="
)

REQUEST_TIMEOUT_SECONDS = float(
    os.getenv("ACDH_ID_RECONCILER_REQUEST_TIMEOUT_SECONDS", "30")
)
DEBUG = os.getenv("ACDH_ID_RECONCILER_DEBUG", False)
ReconciliationResult = dict[str, str]


def _qid_to_uri(qid: str) -> str:
    return f"http://www.wikidata.org/entity/{qid}"


def _run_wikidata_api_query(
    params: Mapping[str, Any], user_agent: str = USER_AGENT
) -> dict[str, Any]:
    headers = {"User-Agent": user_agent, "Accept-Encoding": "gzip"}
    response = requests.get(
        WIKIAPI_BASE,
        params=params,
        headers=headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    if DEBUG:
        print(response.url)
    return response.json()


def _first_qid_for_claim(
    wiki_property: str, value: str, user_agent: str = USER_AGENT
) -> str | None:
    data = _run_wikidata_api_query(
        {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": f"haswbstatement:{wiki_property}={value}",
            "srlimit": 5,
        },
        user_agent=user_agent,
    )
    results = data.get("query", {}).get("search", [])
    for item in results:
        qid = item.get("title", "")
        if qid.startswith("Q"):
            return qid
    return None


def _entity_by_qid(
    qid: str, user_agent: str = USER_AGENT, props: str = "claims"
) -> dict[str, Any]:
    data = _run_wikidata_api_query(
        {
            "action": "wbgetentities",
            "format": "json",
            "ids": qid,
            "props": props,
        },
        user_agent=user_agent,
    )
    return data.get("entities", {}).get(qid, {})


def _claim_value_to_string(value: Any) -> str | None:
    if isinstance(value, (str, int, float)):
        return str(value)

    if isinstance(value, dict):
        if "id" in value:
            return _qid_to_uri(value["id"])
        if "numeric-id" in value:
            entity_type = value.get("entity-type", "item")
            prefix = "Q" if entity_type == "item" else "P"
            return _qid_to_uri(f"{prefix}{value['numeric-id']}")
        if "text" in value:
            return str(value["text"])
        if "time" in value:
            return str(value["time"])

    return None


def _first_claim(entity: Mapping[str, Any], wiki_property: str) -> str | None:
    claims = entity.get("claims", {}).get(wiki_property, [])
    for statement in claims:
        mainsnak = statement.get("mainsnak", {})
        datavalue = mainsnak.get("datavalue")
        if not datavalue:
            continue
        parsed = _claim_value_to_string(datavalue.get("value"))
        if parsed is not None:
            return parsed
    return None


def gnd_to_wikidata(gnd: str, user_agent: str = USER_AGENT) -> ReconciliationResult:
    norm_id = get_norm_id(gnd)
    qid = _first_qid_for_claim("P227", norm_id, user_agent=user_agent)
    if not qid:
        return {}

    return {"wikidata": _qid_to_uri(qid), "gnd": norm_id}


def gnd_to_geonames(gnd: str, user_agent: str = USER_AGENT) -> ReconciliationResult:
    norm_id = get_norm_id(gnd)
    qid = _first_qid_for_claim("P227", norm_id, user_agent=user_agent)
    if not qid:
        return {}

    entity = _entity_by_qid(qid, user_agent=user_agent, props="claims")
    geonames_value = _first_claim(entity, "P1566")
    if geonames_value is None:
        return {}

    gnd_value = _first_claim(entity, "P227") or norm_id
    return {
        "wikidata": _qid_to_uri(qid),
        "gnd": gnd_value,
        "geonames": geonames_value,
    }


def geonames_to_gnd(
    geonames: str, user_agent: str = USER_AGENT
) -> ReconciliationResult:
    norm_id = get_norm_id(geonames)
    qid = _first_qid_for_claim("P1566", norm_id, user_agent=user_agent)
    if not qid:
        return {}

    entity = _entity_by_qid(qid, user_agent=user_agent, props="claims")
    gnd_value = _first_claim(entity, "P227")
    if gnd_value is None:
        return {}

    geonames_value = _first_claim(entity, "P1566") or norm_id
    return {
        "wikidata": _qid_to_uri(qid),
        "geonames": geonames_value,
        "gnd": gnd_value,
    }


def geonames_to_wikidata(
    geonames: str, user_agent: str = USER_AGENT
) -> ReconciliationResult:
    norm_id = get_norm_id(geonames)
    qid = _first_qid_for_claim("P1566", norm_id, user_agent=user_agent)
    if not qid:
        return {}

    return {"wikidata": _qid_to_uri(qid), "geonames": norm_id}


def wikidata_to_wikipedia(
    wikidata_uri: str, user_agent: str = USER_AGENT, wiki_lang: str = "dewiki"
) -> str:
    wiki_id = normalize_wikidata_id(wikidata_uri)
    query_url = f"{WIKIAPI_URL}{wiki_id}&sitefilter={wiki_lang}"
    r = requests.get(
        query_url,
        headers={"User-Agent": user_agent, "Accept-Encoding": "gzip"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    r.raise_for_status()
    result = r.json()
    wikipedia_url = result["entities"][wiki_id]["sitelinks"][wiki_lang]["url"]
    return wikipedia_url


def gnd_to_wikidata_custom(
    gnd: str, wiki_property: str, user_agent: str = USER_AGENT
) -> ReconciliationResult:
    norm_id = get_norm_id(gnd)
    qid = _first_qid_for_claim("P227", norm_id, user_agent=user_agent)
    if not qid:
        return {}

    entity = _entity_by_qid(qid, user_agent=user_agent, props="claims")
    result = {
        "wikidata": _qid_to_uri(qid),
        "gnd": _first_claim(entity, "P227") or norm_id,
    }
    custom_value = _first_claim(entity, wiki_property)
    if custom_value is not None:
        result["custom"] = custom_value
    return result
