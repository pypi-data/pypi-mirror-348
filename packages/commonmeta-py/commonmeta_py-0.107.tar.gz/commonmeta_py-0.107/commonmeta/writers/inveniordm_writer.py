"""InvenioRDM writer for commonmeta-py"""

from typing import Optional

import orjson as json

from ..base_utils import compact, parse_attributes, presence, wrap
from ..constants import (
    CM_TO_INVENIORDM_TRANSLATIONS,
    CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS,
    INVENIORDM_IDENTIFIER_TYPES,
)
from ..date_utils import get_iso8601_date
from ..doi_utils import doi_from_url, normalize_doi
from ..utils import (
    FOS_MAPPINGS,
    get_language,
    id_from_url,
    normalize_url,
    validate_orcid,
    validate_ror,
)


def write_inveniordm(metadata):
    """Write inveniordm"""
    if metadata is None or metadata.write_errors is not None:
        return None
    _type = CM_TO_INVENIORDM_TRANSLATIONS.get(metadata.type, "Other")
    creators = [
        to_inveniordm_creator(i)
        for i in wrap(metadata.contributors)
        if i.get("contributorRoles", None) == ["Author"]
    ]
    identifiers = [
        {
            "identifier": i.get("identifier", None),
            "scheme": INVENIORDM_IDENTIFIER_TYPES.get(
                i.get("identifierType", None), "other"
            ),
        }
        for i in wrap(metadata.identifiers)
        if i.get("identifierType", None) != "DOI"
    ]
    identifiers.append(
        {
            "identifier": metadata.url,
            "scheme": "url",
        }
    )
    references = [to_inveniordm_reference(i) for i in wrap(metadata.references)]
    related_identifiers = [
        to_inveniordm_related_identifier(i)
        for i in wrap(metadata.relations)
        if i.get("id", None) and i.get("type", None) != "IsPartOf"
    ]
    funding = compact(
        [
            to_inveniordm_funding(i)
            for i in wrap(metadata.funding_references)
            if i.get("funderName", None)
        ]
    )
    container = metadata.container if metadata.container else {}
    journal = (
        container.get("title", None)
        if _type not in ["inbook", "inproceedings"]
        and container.get("type") in ["Journal", "Periodical", "Blog"]
        else None
    )
    issn = (
        container.get("identifier", None)
        if container.get("identifierType", None) == "ISSN"
        else None
    )
    dates = []
    for date in metadata.date.keys():
        if metadata.date.get(date, None) is None:
            continue
        t = date.lower()
        if t == "published":
            t = "issued"
        elif t == "accessed":
            t = "other"
        dates.append(
            {
                "date": metadata.date.get(date),
                "type": {"id": t},
            }
        )

    subjects = [to_inveniordm_subject(i) for i in wrap(metadata.subjects)]
    data = compact(
        {
            "pids": {
                "doi": {
                    "identifier": doi_from_url(metadata.id),
                    "provider": "external",
                },
            },
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": False},
            "metadata": compact(
                {
                    "resource_type": {"id": _type},
                    "creators": creators,
                    "title": parse_attributes(
                        metadata.titles, content="title", first=True
                    ),
                    "publisher": metadata.publisher.get("name", None)
                    if metadata.publisher
                    else None,
                    "publication_date": get_iso8601_date(metadata.date.get("published"))
                    if metadata.date.get("published", None)
                    else None,
                    "dates": presence(dates),
                    "subjects": presence(subjects),
                    "description": parse_attributes(
                        metadata.descriptions, content="description", first=True
                    ),
                    "rights": [{"id": metadata.license.get("id").lower()}]
                    if metadata.license.get("id", None)
                    else None,
                    "languages": [
                        {"id": get_language(metadata.language, format="alpha_3")}
                    ]
                    if metadata.language
                    else None,
                    "identifiers": identifiers,
                    "references": presence(references),
                    "related_identifiers": presence(related_identifiers),
                    "funding": presence(funding),
                    "version": metadata.version,
                }
            ),
            "custom_fields": compact(
                {
                    "journal:journal": compact({"title": journal, "issn": issn}),
                    "rs:content_html": presence(metadata.content),
                    "rs:image": presence(metadata.image),
                    "rs:generator": container.get("platform", None),
                }
            ),
        }
    )
    return json.dumps(data, option=json.OPT_INDENT_2)


def to_inveniordm_creator(creator: dict) -> dict:
    """Convert creators to inveniordm creators"""

    def format_identifier(id):
        identifier = validate_orcid(id)
        if identifier:
            return [
                {
                    "identifier": identifier,
                    "scheme": "orcid",
                }
            ]
        return None

    _type = creator.get("type", None)
    if creator.get("familyName", None):
        name = ", ".join([creator.get("familyName", ""), creator.get("givenName", "")])
    elif creator.get("name", None):
        name = creator.get("name", None)

    return compact(
        {
            "person_or_org": compact(
                {
                    "name": name,
                    "given_name": creator.get("givenName", None),
                    "family_name": creator.get("familyName", None),
                    "type": _type.lower() + "al" if _type else None,
                    "identifiers": format_identifier(creator.get("id", None)),
                }
            ),
            "affiliations": to_inveniordm_affiliations(creator),
        }
    )


def to_inveniordm_subject(sub: dict) -> Optional[dict]:
    """Convert subject to inveniordm subject"""
    if sub.get("subject", None) is None:
        return None
    if sub.get("subject").startswith("FOS: "):
        subject = sub.get("subject")[5:]
        id_ = FOS_MAPPINGS.get(subject, None)
        return compact(
            {
                "id": id_,
                "subject": subject,
            }
        )
    return compact(
        {
            "subject": sub.get("subject"),
        }
    )


def to_inveniordm_affiliations(creator: dict) -> Optional[list]:
    """Convert affiliations to inveniordm affiliations.
    Returns None if creator is not a person."""

    def format_affiliation(affiliation):
        return compact(
            {
                "id": id_from_url(affiliation.get("id", None)),
                "name": affiliation.get("name", None),
            }
        )

    if creator.get("type", None) != "Person":
        return None

    return compact(
        [format_affiliation(i) for i in wrap(creator.get("affiliations", None))]
    )


def to_inveniordm_related_identifier(relation: dict) -> dict:
    """Convert relation to inveniordm related_identifier"""
    if normalize_doi(relation.get("id", None)):
        identifier = doi_from_url(relation.get("id", None))
        scheme = "doi"
    elif normalize_url(relation.get("id", None)):
        identifier = relation.get("id", None)
        scheme = "url"
    else:
        return None

    # normalize relation types
    relation_type = relation.get("type")
    if relation.get("type") == "HasReview":
        relation_type = "IsReviewedBy"
    elif relation.get("type") == "IsPreprintOf":
        relation_type = "IsPreviousVersionOf"

    return compact(
        {
            "identifier": identifier,
            "scheme": scheme,
            "relation_type": {
                "id": relation_type.lower(),
            },
        }
    )


def to_inveniordm_reference(reference: dict) -> dict:
    """Convert reference to inveniordm reference"""
    if normalize_doi(reference.get("id", None)):
        identifier = doi_from_url(reference.get("id", None))
        scheme = "doi"
    elif normalize_url(reference.get("id", None)):
        identifier = reference.get("id", None)
        scheme = "url"
    else:
        identifier = None
        scheme = None

    if reference.get("unstructured", None) is None:
        # use title as unstructured reference
        if reference.get("title", None):
            unstructured = reference.get("title")
        else:
            unstructured = "Unknown title"

        if reference.get("publicationYear", None):
            unstructured += " (" + reference.get("publicationYear") + ")."

        return compact(
            {
                "reference": unstructured,
                "scheme": scheme,
                "identifier": identifier,
            }
        )
    else:
        unstructured = reference.get("unstructured")

        if reference.get("id", None):
            # remove duplicate ID from unstructured reference
            unstructured = unstructured.replace(reference.get("id"), "")

        # remove optional trailing whitespace
        unstructured = unstructured.rstrip()

        return compact(
            {
                "reference": unstructured,
                "scheme": scheme,
                "identifier": identifier,
            }
        )


def to_inveniordm_funding(funding: dict) -> Optional[dict]:
    """Convert funding to inveniordm funding"""
    if funding.get("funderIdentifierType", None) == "Crossref Funder ID":
        # convert to ROR
        funder_identifier = id_from_url(
            CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS.get(
                funding.get("funderIdentifier", None), None
            )
        )
    else:
        funder_identifier = validate_ror(funding.get("funderIdentifier", None))
    award_number = funding.get("awardNumber", None)
    award_title = funding.get("awardTitle", None)
    if award_title:
        award_title = {"en": award_title}
    if funding.get("awardUri", None):
        award_identifier = funding.get("awardUri", None)
        scheme = "doi" if normalize_doi(award_identifier) else "url"
        if scheme == "doi":
            award_identifier = doi_from_url(award_identifier)
        award_identifiers = [
            {
                "scheme": scheme,
                "identifier": award_identifier,
            },
        ]
    else:
        award_identifiers = None

    if award_number or award_title or award_identifiers:
        return compact(
            {
                "funder": compact(
                    {
                        "name": funding.get("funderName"),
                        "id": funder_identifier,
                    }
                ),
                "award": compact(
                    {
                        "number": award_number,
                        "title": award_title,
                        "identifiers": award_identifiers,
                    }
                ),
            }
        )

    return compact(
        {
            "funder": compact(
                {
                    "name": funding.get("funderName"),
                    "id": funder_identifier,
                }
            ),
        }
    )
