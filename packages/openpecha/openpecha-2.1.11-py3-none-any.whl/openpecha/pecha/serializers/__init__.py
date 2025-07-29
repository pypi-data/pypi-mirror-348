from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel
from openpecha.pecha.metadata import Language
from openpecha.pecha.pecha_types import PechaType, get_pecha_type
from openpecha.pecha.serializers.pecha_db import Serializer
from openpecha.pecha.serializers.pecha_db.utils import FormatPechaCategory
from openpecha.pecha.serializers.utils import (
    find_related_pecha_id,
    get_metadatachain_from_metadatatree,
)
from openpecha.utils import chunk_strings


class BaseSerializer(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def serialize(
        self,
        pecha_path: Path,
        source_type: str,
    ):
        pass


def modify_root_title_mapping(serialized_json: Dict, pecha: Pecha):
    # Change the Title mapping
    title = pecha.metadata.title["en"]

    serialized_json["source"]["categories"][-1]["base_text_titles"] = [title]
    serialized_json["target"]["categories"][-1]["base_text_titles"] = [title]
    return serialized_json


def assign_lang_code_to_title(serialized_json: Dict):
    source_title = serialized_json["source"]["books"][0]["title"]
    lang = serialized_json["source"]["books"][0]["language"]

    if lang != Language.english.value:
        serialized_json["source"]["books"][0]["title"] = f"{source_title} [{lang}]"

    return serialized_json


def reset_target_to_empty_chinese(target_book: Dict, lzh_title: Optional[str] = None):
    target_book["title"] = lzh_title
    target_book["language"] = Language.literal_chinese.value
    target_book["versionSource"] = ""
    target_book["content"] = []


def get_pecha_segments(pecha: Pecha) -> List[Dict[str, str]]:
    base_name = list(pecha.bases.keys())[0]
    segments = []
    for _, ann_store in pecha.get_layers(base_name=base_name):
        for ann in list(ann_store):
            segment_text = ann.text()[0]
            segments.append(segment_text)
    return chunk_strings(segments)


def _serialize_root_pecha(
    serialized_json: Dict,
    pecha: Pecha,
    pecha_category: List[Dict[str, Dict]],
    pecha_chain: List[Pecha],
):
    source_book = {
        "title": pecha.metadata.title[Language.tibetan.value],
        "language": Language.tibetan.value,
        "versionSource": pecha.metadata.source if pecha.metadata.source else "",
        "direction": "ltr",
        "completestatus": "done",
        "content": serialized_json["target"]["books"][0]["content"],
    }
    target_book = {
        "title": pecha.metadata.title[pecha.metadata.language.value],
        "language": pecha.metadata.language.value,
        "versionSource": pecha.metadata.source if pecha.metadata.source else "",
        "direction": "ltr",
        "completestatus": "done",
        "content": get_pecha_segments(pecha),
    }
    category = FormatPechaCategory().format_root_category(pecha, pecha_category)
    serialized_json["source"]["books"][0] = source_book
    serialized_json["target"]["books"][0] = target_book
    serialized_json["source"]["categories"] = category["en"]
    serialized_json["target"]["categories"] = category["lzh"]
    return serialized_json


def _serialize_root_translation_pecha(
    serialized_json: Dict,
    pecha: Pecha,
    pecha_category: List[Dict[str, Dict]],
    pecha_chain: List[Pecha],
):
    if (
        serialized_json["source"]["books"][0]["language"]
        == Language.literal_chinese.value
    ):
        source_book = {
            "title": pecha.metadata.title[Language.english.value],
            "language": Language.english.value,
            "versionSource": "",
            "direction": "ltr",
            "completestatus": "done",
            "content": [],
        }
        target_book = serialized_json["source"]["books"][0]
    else:
        source_book = serialized_json["source"]["books"][0]
        target_book = {
            "title": pecha.metadata.title[Language.literal_chinese.value],
            "language": Language.literal_chinese.value,
            "versionSource": pecha.metadata.source if pecha.metadata.source else "",
            "direction": "ltr",
            "completestatus": "done",
            "content": get_pecha_segments(pecha),
        }
    serialized_json["target"]["books"][0] = target_book
    serialized_json["source"]["books"][0] = source_book

    category = FormatPechaCategory().format_root_category(pecha, pecha_category)
    serialized_json["source"]["categories"] = category["en"]
    serialized_json["target"]["categories"] = category["lzh"]
    return serialized_json


def _serialize_commentary_pecha(
    serialized_json: Dict,
    pecha: Pecha,
    pecha_category: List[Dict[str, Dict]],
    pecha_chain: List[Pecha],
) -> Dict:
    # Modify the Pecha Category
    commentary_pecha, root_pecha = pecha_chain[0], pecha_chain[1]
    root_title = root_pecha.metadata.title.get("en", "")
    category = FormatPechaCategory().format_commentary_category(
        commentary_pecha, pecha_category, root_title
    )

    serialized_json = modify_root_title_mapping(serialized_json, pecha)

    source_book = serialized_json["source"]["books"][0]
    target_book = serialized_json["target"]["books"][0]
    tgt_content = target_book.get("content", [])

    commentary_lzh_title = commentary_pecha.metadata.title.get("lzh", "")

    if tgt_content:
        # Move target to source, reset target
        serialized_json["source"]["books"][0] = deepcopy(target_book)
        reset_target_to_empty_chinese(target_book, commentary_lzh_title)

    else:
        src_lang = source_book.get("language")
        if src_lang == Language.literal_chinese.value:
            # Swap source and target
            serialized_json["target"]["books"][0] = deepcopy(source_book)
            serialized_json["source"]["books"][0] = {
                "title": commentary_pecha.metadata.title.get("en", ""),
                "language": Language.english.value,
                "versionSource": commentary_pecha.metadata.source
                if commentary_pecha.metadata.source
                else "",
                "direction": "ltr",
                "completestatus": "done",
                "content": [],
            }
        else:
            reset_target_to_empty_chinese(target_book, commentary_lzh_title)

    serialized_json["source"]["categories"] = category["en"]
    serialized_json["target"]["categories"] = category["lzh"]

    return serialized_json


def _serialize_commentary_translation_pecha(
    serialized_json: Dict,
    pecha: Pecha,
    pecha_category: List[Dict[str, Dict]],
    pecha_chain: List[Pecha],
):
    """
    1. Modify the Title Mapping
    2. Remove the tibetan content from the `target` field from serialized_json.
    """
    # Modify the Pecha Category
    commentary_pecha, root_pecha = pecha_chain[1], pecha_chain[2]
    root_title = root_pecha.metadata.title.get("en", "")
    category = FormatPechaCategory().format_commentary_category(
        commentary_pecha, pecha_category, root_title
    )
    serialized_json["source"]["categories"] = category["en"]
    serialized_json["target"]["categories"] = category["lzh"]

    serialized = modify_root_title_mapping(serialized_json, pecha)

    source_book = serialized_json["source"]["books"][0]
    target_book = serialized_json["target"]["books"][0]

    if source_book["language"] == Language.literal_chinese.value:
        serialized["target"]["books"][0] = deepcopy(source_book)
        serialized["source"]["books"][0] = {
            "title": commentary_pecha.metadata.title.get("en", ""),
            "language": Language.english.value,
            "versionSource": commentary_pecha.metadata.source
            if commentary_pecha.metadata.source
            else "",
            "direction": "ltr",
            "completestatus": "done",
            "content": [],
        }

        return serialized

    commentary_lzh_title = commentary_pecha.metadata.title.get("lzh", "")
    reset_target_to_empty_chinese(target_book, commentary_lzh_title)

    return serialized


def _serialize_prealigned_commentary_pecha(
    serialized_json: Dict,
    pecha: Pecha,
    pecha_category: List[Dict[str, Dict]],
    pecha_chain: List[Pecha],
) -> Dict:
    # Modify the Pecha Category
    commentary_pecha, root_pecha = pecha_chain[0], pecha_chain[1]
    root_title = root_pecha.metadata.title.get("en", "")
    category = FormatPechaCategory().format_commentary_category(
        commentary_pecha, pecha_category, root_title
    )

    serialized = modify_root_title_mapping(serialized_json, pecha)

    target_book = serialized_json["target"]["books"][0]

    serialized["source"]["books"][0] = deepcopy(target_book)

    commentary_lzh_title = commentary_pecha.metadata.title.get("lzh", "")
    reset_target_to_empty_chinese(target_book, commentary_lzh_title)

    serialized["source"]["categories"] = category["en"]
    serialized["target"]["categories"] = category["lzh"]

    return serialized


PECHA_SERIALIZER_REGISTRY = {
    PechaType.root_pecha: _serialize_root_pecha,
    PechaType.root_translation_pecha: _serialize_root_translation_pecha,
    PechaType.commentary_pecha: _serialize_commentary_pecha,
    PechaType.commentary_translation_pecha: _serialize_commentary_translation_pecha,
    PechaType.prealigned_commentary_pecha: _serialize_prealigned_commentary_pecha,
    PechaType.prealigned_root_translation_pecha: _serialize_root_translation_pecha,
}


class SerializerLogicHandler:
    @staticmethod
    def get_root_translation_pecha_id(
        metadatatree: List[Any], pecha_id: str, lang: str
    ) -> Optional[str]:
        """
        1. Get metadata chain from metadata tree
        2. Get Root pecha. (last element of metadata chain)
        3. Get Root Translation Pecha id by comparing with lang given.
            i.e if lang = 'lzh', get lzh root translation pecha
        """
        metadata_chain = get_metadatachain_from_metadatatree(metadatatree, pecha_id)
        root_pecha_id = metadata_chain[-1].id

        for metadata in metadatatree:
            if metadata.language == lang and metadata.translation_of == root_pecha_id:
                return metadata.id

        return None

    def serialize(
        self,
        pechatree: Dict[str, Pecha],
        metadatatree: List[Any],
        annotations: Dict[str, List[AnnotationModel]],
        pecha_category: List[Dict[str, Dict[str, str]]],
        annotation_path: str,
        base_language: str,
    ):
        pecha_id = find_related_pecha_id(annotations, annotation_path)
        if not pecha_id:
            raise ValueError(
                f"Annotation path: {annotation_path} is not present in any of Annotations: {annotations}."
            )
        metadata_chain = get_metadatachain_from_metadatatree(metadatatree, pecha_id)
        pecha_chain = [pechatree[metadata.id] for metadata in metadata_chain]  # noqa

        root_pecha_lang = metadata_chain[-1].language
        if root_pecha_lang not in [
            Language.tibetan.value,
            Language.literal_chinese.value,
        ]:
            raise ValueError(
                f"Pecha id: {pecha_id} points to Root Pecha: {metadata_chain[-1].id} where it language is {root_pecha_lang}.Language should be from 'bo' or 'lzh'."
            )

        pecha_type = get_pecha_type(
            pecha_chain, metadata_chain, annotations, annotation_path
        )
        match base_language:
            case Language.tibetan.value:
                # pecha.org website centered around bo Root text.
                if root_pecha_lang == Language.tibetan.value:
                    return Serializer().serialize(
                        pecha_chain,
                        metadata_chain,
                        annotations,
                        pecha_category,
                        annotation_path,
                    )
                if root_pecha_lang == Language.literal_chinese.value:
                    pass

            case Language.literal_chinese.value:
                # fodian.org website centered around lzh Root text.
                if root_pecha_lang == Language.tibetan.value:
                    serialized = Serializer().serialize(
                        pecha_chain,
                        metadata_chain,
                        annotations,
                        pecha_category,
                        annotation_path,
                    )
                    lzh_root_pecha_id = self.get_root_translation_pecha_id(
                        metadatatree, pecha_id, Language.literal_chinese.value
                    )
                    if not lzh_root_pecha_id:
                        raise ValueError(
                            f"literal Chinese Pecha no where present in MetadataTree: {metadatatree}."
                        )
                    lzh_root_pecha = pechatree[lzh_root_pecha_id]

                    handler = PECHA_SERIALIZER_REGISTRY.get(pecha_type)
                    if not handler:
                        raise ValueError(f"Unsupported pecha type: {pecha_type}")
                    return assign_lang_code_to_title(
                        handler(serialized, lzh_root_pecha, pecha_category, pecha_chain)
                    )

                if root_pecha_lang == Language.literal_chinese.value:
                    pass

            case _:
                raise ValueError(
                    f"Invalid base language {base_language} is passed for Serialization. Should be from 'bo' or 'lzh'."
                )
        pass
