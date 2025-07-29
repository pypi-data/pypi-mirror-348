"""Contains all the data models used in inputs/outputs"""

from .ack import Ack
from .aggregation import Aggregation
from .alt_text import AltText
from .annotate_binary_form import AnnotateBinaryForm
from .annotate_binary_with_project_annotator_body import (
    AnnotateBinaryWithProjectAnnotatorBody,
)
from .annotate_binary_with_project_body import AnnotateBinaryWithProjectBody
from .annotate_documents_with_pipeline import AnnotateDocumentsWithPipeline
from .annotate_format_binary_with_project_annotator_body import (
    AnnotateFormatBinaryWithProjectAnnotatorBody,
)
from .annotate_text_with_pipeline import AnnotateTextWithPipeline
from .annotated_doc_alt_text import AnnotatedDocAltText
from .annotated_doc_annotation import AnnotatedDocAnnotation
from .annotated_doc_annotation_creation_mode import AnnotatedDocAnnotationCreationMode
from .annotated_doc_annotation_properties import AnnotatedDocAnnotationProperties
from .annotated_doc_category import AnnotatedDocCategory
from .annotated_doc_category_creation_mode import AnnotatedDocCategoryCreationMode
from .annotated_doc_category_properties import AnnotatedDocCategoryProperties
from .annotated_doc_sentence import AnnotatedDocSentence
from .annotated_doc_sentence_metadata import AnnotatedDocSentenceMetadata
from .annotated_document import AnnotatedDocument
from .annotated_document_metadata import AnnotatedDocumentMetadata
from .annotation import Annotation
from .annotation_creation_mode import AnnotationCreationMode
from .annotation_facets import AnnotationFacets
from .annotation_id import AnnotationId
from .annotation_metrics import AnnotationMetrics
from .annotation_patch import AnnotationPatch
from .annotation_patch_status import AnnotationPatchStatus
from .annotation_plan import AnnotationPlan
from .annotation_status import AnnotationStatus
from .annotation_term import AnnotationTerm
from .annotation_term_properties import AnnotationTermProperties
from .annotator import Annotator
from .annotator_multimap import AnnotatorMultimap
from .app_config import AppConfig
from .apply_to import ApplyTo
from .batch_chown_chmod import BatchChownChmod
from .batch_chown_chmod_migration import BatchChownChmodMigration
from .batch_chown_chmod_result import BatchChownChmodResult
from .batch_chown_chmod_virtual_target_users_item import (
    BatchChownChmodVirtualTargetUsersItem,
)
from .batch_errors import BatchErrors
from .batch_migration_operation import BatchMigrationOperation
from .batch_migration_operation_users import BatchMigrationOperationUsers
from .batch_migration_receive import BatchMigrationReceive
from .bearer_token import BearerToken
from .bucket import Bucket
from .categories_facets import CategoriesFacets
from .category import Category
from .category_action import CategoryAction
from .category_creation_mode import CategoryCreationMode
from .category_id import CategoryId
from .category_metrics import CategoryMetrics
from .category_patch import CategoryPatch
from .category_patch_status import CategoryPatchStatus
from .category_status import CategoryStatus
from .classification_config import ClassificationConfig
from .classification_options import ClassificationOptions
from .config_patch_options import ConfigPatchOptions
from .convert_annotation_plan import ConvertAnnotationPlan
from .convert_format_annotation_plan import ConvertFormatAnnotationPlan
from .converter import Converter
from .converter_parameters import ConverterParameters
from .corpus_metrics import CorpusMetrics
from .create_lexicon_response_200 import CreateLexiconResponse200
from .create_project_from_archive_body import CreateProjectFromArchiveBody
from .create_term_body import CreateTermBody
from .create_term_response_200 import CreateTermResponse200
from .create_theme_form import CreateThemeForm
from .create_theme_from_archive_body import CreateThemeFromArchiveBody
from .created_by_count import CreatedByCount
from .credentials import Credentials
from .default_annotation_plan import DefaultAnnotationPlan
from .default_processor_context import DefaultProcessorContext
from .delete_group_result import DeleteGroupResult
from .delete_many_response import DeleteManyResponse
from .delete_response import DeleteResponse
from .deprecated_annotate_binary_with_plan_ref_body import (
    DeprecatedAnnotateBinaryWithPlanRefBody,
)
from .deprecated_annotate_format_binary_with_plan_ref_body import (
    DeprecatedAnnotateFormatBinaryWithPlanRefBody,
)
from .doc_alt_text import DocAltText
from .doc_annotation import DocAnnotation
from .doc_annotation_creation_mode import DocAnnotationCreationMode
from .doc_annotation_properties import DocAnnotationProperties
from .doc_annotation_status import DocAnnotationStatus
from .doc_category import DocCategory
from .doc_category_creation_mode import DocCategoryCreationMode
from .doc_category_properties import DocCategoryProperties
from .doc_category_status import DocCategoryStatus
from .doc_sentence import DocSentence
from .doc_sentence_metadata import DocSentenceMetadata
from .document import Document
from .document_facets import DocumentFacets
from .document_hit import DocumentHit
from .document_hits import DocumentHits
from .document_metadata import DocumentMetadata
from .engine_config import EngineConfig
from .engine_config_import_summary import EngineConfigImportSummary
from .engine_name import EngineName
from .error import Error
from .experiment import Experiment
from .experiment_parameters import ExperimentParameters
from .experiment_patch import ExperimentPatch
from .experiment_patch_parameters import ExperimentPatchParameters
from .export_terms_response_200_item import ExportTermsResponse200Item
from .external_databases import ExternalDatabases
from .external_resources import ExternalResources
from .filtering_params import FilteringParams
from .find_similar_segments_search_type import FindSimilarSegmentsSearchType
from .format_binary_form import FormatBinaryForm
from .format_documents_with_many import FormatDocumentsWithMany
from .format_text_with_many import FormatTextWithMany
from .formatter import Formatter
from .formatter_parameters import FormatterParameters
from .gazetteer import Gazetteer
from .gazetteer_parameters import GazetteerParameters
from .gazetteer_patch import GazetteerPatch
from .gazetteer_patch_parameters import GazetteerPatchParameters
from .general_app_bar import GeneralAppBar
from .general_config import GeneralConfig
from .general_footer import GeneralFooter
from .general_toolbar import GeneralToolbar
from .get_base_theme_config_response_200 import GetBaseThemeConfigResponse200
from .get_favorite_theme_scope import GetFavoriteThemeScope
from .get_global_messages_scopes_item import GetGlobalMessagesScopesItem
from .get_term_response_200 import GetTermResponse200
from .get_theme_config_schema_response_200 import GetThemeConfigSchemaResponse200
from .get_themes_scope import GetThemesScope
from .group_desc import GroupDesc
from .group_desc_mapping_discriminator import GroupDescMappingDiscriminator
from .group_name import GroupName
from .group_patch import GroupPatch
from .group_patch_mapping_discriminator import GroupPatchMappingDiscriminator
from .group_share import GroupShare
from .http_service_metadata import HttpServiceMetadata
from .http_service_metadata_operations import HttpServiceMetadataOperations
from .http_service_metadata_service import HttpServiceMetadataService
from .http_service_record import HttpServiceRecord
from .import_archive_body import ImportArchiveBody
from .import_models_body import ImportModelsBody
from .imported_doc_annotation import ImportedDocAnnotation
from .imported_doc_annotation_creation_mode import ImportedDocAnnotationCreationMode
from .imported_doc_annotation_properties import ImportedDocAnnotationProperties
from .imported_doc_category import ImportedDocCategory
from .imported_doc_category_creation_mode import ImportedDocCategoryCreationMode
from .imported_doc_category_properties import ImportedDocCategoryProperties
from .imported_document import ImportedDocument
from .imported_document_metadata import ImportedDocumentMetadata
from .index_document_indexes_item import IndexDocumentIndexesItem
from .input_document import InputDocument
from .input_document_metadata import InputDocumentMetadata
from .item_count import ItemCount
from .item_ref import ItemRef
from .label import Label
from .label_count import LabelCount
from .label_names import LabelNames
from .label_set import LabelSet
from .label_set_update import LabelSetUpdate
from .label_update import LabelUpdate
from .launch_document_import_body import LaunchDocumentImportBody
from .launch_document_import_segmentation_policy import (
    LaunchDocumentImportSegmentationPolicy,
)
from .launch_json_documents_import_segmentation_policy import (
    LaunchJsonDocumentsImportSegmentationPolicy,
)
from .launch_project_restoration_from_backup_body import (
    LaunchProjectRestorationFromBackupBody,
)
from .launch_uploaded_document_import_segmentation_policy import (
    LaunchUploadedDocumentImportSegmentationPolicy,
)
from .lexicon import Lexicon
from .lexicon_update import LexiconUpdate
from .localized_message import LocalizedMessage
from .maybe_create_projects_and_import_models_from_archive_body import (
    MaybeCreateProjectsAndImportModelsFromArchiveBody,
)
from .message import Message
from .message_audience import MessageAudience
from .message_id import MessageId
from .message_localized import MessageLocalized
from .message_mark import MessageMark
from .message_patch import MessagePatch
from .message_patch_localized import MessagePatchLocalized
from .message_patch_template import MessagePatchTemplate
from .message_template import MessageTemplate
from .metadata_count import MetadataCount
from .model_metrics import ModelMetrics
from .model_metrics_options import ModelMetricsOptions
from .models_metrics import ModelsMetrics
from .named_annotation_plan import NamedAnnotationPlan
from .named_vector import NamedVector
from .named_vector_creation_mode import NamedVectorCreationMode
from .named_vector_properties import NamedVectorProperties
from .new_experiment import NewExperiment
from .new_experiment_parameters import NewExperimentParameters
from .new_gazetteer import NewGazetteer
from .new_gazetteer_parameters import NewGazetteerParameters
from .new_group_desc import NewGroupDesc
from .new_group_desc_mapping_discriminator import NewGroupDescMappingDiscriminator
from .new_message import NewMessage
from .new_message_localized import NewMessageLocalized
from .new_message_template import NewMessageTemplate
from .new_named_annotation_plan import NewNamedAnnotationPlan
from .new_role import NewRole
from .new_suggester import NewSuggester
from .new_suggester_parameters import NewSuggesterParameters
from .new_theme import NewTheme
from .new_user import NewUser
from .operation_count import OperationCount
from .output_params import OutputParams
from .ownership_change import OwnershipChange
from .partial_label import PartialLabel
from .partial_lexicon import PartialLexicon
from .plan_operation_response import PlanOperationResponse
from .plan_patch import PlanPatch
from .platform_share import PlatformShare
from .project_annotators import ProjectAnnotators
from .project_bean import ProjectBean
from .project_config_creation import ProjectConfigCreation
from .project_config_creation_properties import ProjectConfigCreationProperties
from .project_open_session import ProjectOpenSession
from .project_open_session_state import ProjectOpenSessionState
from .project_property import ProjectProperty
from .project_status import ProjectStatus
from .project_user_share import ProjectUserShare
from .projects_annotators import ProjectsAnnotators
from .quality_figures import QualityFigures
from .question_answering_params import QuestionAnsweringParams
from .question_answering_params_language_detection import (
    QuestionAnsweringParamsLanguageDetection,
)
from .report import Report
from .report_classes import ReportClasses
from .request_jwt_token_project_access_mode import RequestJwtTokenProjectAccessMode
from .role_desc import RoleDesc
from .role_update import RoleUpdate
from .search_documents_search_type import SearchDocumentsSearchType
from .search_filter import SearchFilter
from .search_filter_filter_selector import SearchFilterFilterSelector
from .search_filter_filter_type import SearchFilterFilterType
from .search_params import SearchParams
from .search_params_type import SearchParamsType
from .search_request import SearchRequest
from .search_segments_search_type import SearchSegmentsSearchType
from .search_terms_search_type import SearchTermsSearchType
from .search_total import SearchTotal
from .search_total_relation import SearchTotalRelation
from .segment import Segment
from .segment_hit import SegmentHit
from .segment_hits import SegmentHits
from .segment_metadata import SegmentMetadata
from .segmenter import Segmenter
from .segmenter_parameters import SegmenterParameters
from .set_theme_as_favorite_scope import SetThemeAsFavoriteScope
from .share_mode import ShareMode
from .sherpa_job_bean import SherpaJobBean
from .sherpa_job_bean_status import SherpaJobBeanStatus
from .sherpa_job_bean_type import SherpaJobBeanType
from .signin_app_bar import SigninAppBar
from .signin_card_form import SigninCardForm
from .signin_card_main_titles import SigninCardMainTitles
from .signin_card_subtitles import SigninCardSubtitles
from .signin_config import SigninConfig
from .signin_footer import SigninFooter
from .simple_group import SimpleGroup
from .simple_group_desc import SimpleGroupDesc
from .simple_group_desc_mapping_discriminator import SimpleGroupDescMappingDiscriminator
from .simple_group_membership_desc import SimpleGroupMembershipDesc
from .simple_metadata import SimpleMetadata
from .simple_user import SimpleUser
from .suggester import Suggester
from .suggester_parameters import SuggesterParameters
from .suggester_patch import SuggesterPatch
from .suggester_patch_parameters import SuggesterPatchParameters
from .suggestion_facets import SuggestionFacets
from .term_hit import TermHit
from .term_hit_term import TermHitTerm
from .term_hits import TermHits
from .term_identifier import TermIdentifier
from .term_import import TermImport
from .term_importer_spec import TermImporterSpec
from .term_importer_spec_parameters import TermImporterSpecParameters
from .text_count import TextCount
from .theme import Theme
from .theme_config import ThemeConfig
from .theme_id import ThemeId
from .theme_media import ThemeMedia
from .theme_update import ThemeUpdate
from .update_theme_form import UpdateThemeForm
from .upload_files_body import UploadFilesBody
from .uploaded_file import UploadedFile
from .uploaded_file_info import UploadedFileInfo
from .user_group_ref import UserGroupRef
from .user_permissions_update import UserPermissionsUpdate
from .user_profile import UserProfile
from .user_profile_update import UserProfileUpdate
from .user_response import UserResponse
from .user_share import UserShare
from .users_response import UsersResponse
from .vector_params import VectorParams
from .vector_params_native_rrf import VectorParamsNativeRRF
from .vuetify_config import VuetifyConfig
from .vuetify_dark_theme import VuetifyDarkTheme
from .vuetify_light_theme import VuetifyLightTheme
from .vuetify_themes import VuetifyThemes
from .with_annotator import WithAnnotator
from .with_annotator_condition import WithAnnotatorCondition
from .with_annotator_parameters import WithAnnotatorParameters
from .with_converter import WithConverter
from .with_converter_condition import WithConverterCondition
from .with_converter_parameters import WithConverterParameters
from .with_language_guesser import WithLanguageGuesser
from .with_language_guesser_condition import WithLanguageGuesserCondition
from .with_language_guesser_parameters import WithLanguageGuesserParameters
from .with_processor import WithProcessor
from .with_processor_condition import WithProcessorCondition
from .with_processor_parameters import WithProcessorParameters
from .with_segmenter import WithSegmenter
from .with_segmenter_condition import WithSegmenterCondition
from .with_segmenter_parameters import WithSegmenterParameters
from .with_vectorizer import WithVectorizer
from .with_vectorizer_condition import WithVectorizerCondition
from .with_vectorizer_parameters import WithVectorizerParameters

__all__ = (
    "Ack",
    "Aggregation",
    "AltText",
    "AnnotateBinaryForm",
    "AnnotateBinaryWithProjectAnnotatorBody",
    "AnnotateBinaryWithProjectBody",
    "AnnotatedDocAltText",
    "AnnotatedDocAnnotation",
    "AnnotatedDocAnnotationCreationMode",
    "AnnotatedDocAnnotationProperties",
    "AnnotatedDocCategory",
    "AnnotatedDocCategoryCreationMode",
    "AnnotatedDocCategoryProperties",
    "AnnotatedDocSentence",
    "AnnotatedDocSentenceMetadata",
    "AnnotatedDocument",
    "AnnotatedDocumentMetadata",
    "AnnotateDocumentsWithPipeline",
    "AnnotateFormatBinaryWithProjectAnnotatorBody",
    "AnnotateTextWithPipeline",
    "Annotation",
    "AnnotationCreationMode",
    "AnnotationFacets",
    "AnnotationId",
    "AnnotationMetrics",
    "AnnotationPatch",
    "AnnotationPatchStatus",
    "AnnotationPlan",
    "AnnotationStatus",
    "AnnotationTerm",
    "AnnotationTermProperties",
    "Annotator",
    "AnnotatorMultimap",
    "AppConfig",
    "ApplyTo",
    "BatchChownChmod",
    "BatchChownChmodMigration",
    "BatchChownChmodResult",
    "BatchChownChmodVirtualTargetUsersItem",
    "BatchErrors",
    "BatchMigrationOperation",
    "BatchMigrationOperationUsers",
    "BatchMigrationReceive",
    "BearerToken",
    "Bucket",
    "CategoriesFacets",
    "Category",
    "CategoryAction",
    "CategoryCreationMode",
    "CategoryId",
    "CategoryMetrics",
    "CategoryPatch",
    "CategoryPatchStatus",
    "CategoryStatus",
    "ClassificationConfig",
    "ClassificationOptions",
    "ConfigPatchOptions",
    "ConvertAnnotationPlan",
    "Converter",
    "ConverterParameters",
    "ConvertFormatAnnotationPlan",
    "CorpusMetrics",
    "CreatedByCount",
    "CreateLexiconResponse200",
    "CreateProjectFromArchiveBody",
    "CreateTermBody",
    "CreateTermResponse200",
    "CreateThemeForm",
    "CreateThemeFromArchiveBody",
    "Credentials",
    "DefaultAnnotationPlan",
    "DefaultProcessorContext",
    "DeleteGroupResult",
    "DeleteManyResponse",
    "DeleteResponse",
    "DeprecatedAnnotateBinaryWithPlanRefBody",
    "DeprecatedAnnotateFormatBinaryWithPlanRefBody",
    "DocAltText",
    "DocAnnotation",
    "DocAnnotationCreationMode",
    "DocAnnotationProperties",
    "DocAnnotationStatus",
    "DocCategory",
    "DocCategoryCreationMode",
    "DocCategoryProperties",
    "DocCategoryStatus",
    "DocSentence",
    "DocSentenceMetadata",
    "Document",
    "DocumentFacets",
    "DocumentHit",
    "DocumentHits",
    "DocumentMetadata",
    "EngineConfig",
    "EngineConfigImportSummary",
    "EngineName",
    "Error",
    "Experiment",
    "ExperimentParameters",
    "ExperimentPatch",
    "ExperimentPatchParameters",
    "ExportTermsResponse200Item",
    "ExternalDatabases",
    "ExternalResources",
    "FilteringParams",
    "FindSimilarSegmentsSearchType",
    "FormatBinaryForm",
    "FormatDocumentsWithMany",
    "Formatter",
    "FormatterParameters",
    "FormatTextWithMany",
    "Gazetteer",
    "GazetteerParameters",
    "GazetteerPatch",
    "GazetteerPatchParameters",
    "GeneralAppBar",
    "GeneralConfig",
    "GeneralFooter",
    "GeneralToolbar",
    "GetBaseThemeConfigResponse200",
    "GetFavoriteThemeScope",
    "GetGlobalMessagesScopesItem",
    "GetTermResponse200",
    "GetThemeConfigSchemaResponse200",
    "GetThemesScope",
    "GroupDesc",
    "GroupDescMappingDiscriminator",
    "GroupName",
    "GroupPatch",
    "GroupPatchMappingDiscriminator",
    "GroupShare",
    "HttpServiceMetadata",
    "HttpServiceMetadataOperations",
    "HttpServiceMetadataService",
    "HttpServiceRecord",
    "ImportArchiveBody",
    "ImportedDocAnnotation",
    "ImportedDocAnnotationCreationMode",
    "ImportedDocAnnotationProperties",
    "ImportedDocCategory",
    "ImportedDocCategoryCreationMode",
    "ImportedDocCategoryProperties",
    "ImportedDocument",
    "ImportedDocumentMetadata",
    "ImportModelsBody",
    "IndexDocumentIndexesItem",
    "InputDocument",
    "InputDocumentMetadata",
    "ItemCount",
    "ItemRef",
    "Label",
    "LabelCount",
    "LabelNames",
    "LabelSet",
    "LabelSetUpdate",
    "LabelUpdate",
    "LaunchDocumentImportBody",
    "LaunchDocumentImportSegmentationPolicy",
    "LaunchJsonDocumentsImportSegmentationPolicy",
    "LaunchProjectRestorationFromBackupBody",
    "LaunchUploadedDocumentImportSegmentationPolicy",
    "Lexicon",
    "LexiconUpdate",
    "LocalizedMessage",
    "MaybeCreateProjectsAndImportModelsFromArchiveBody",
    "Message",
    "MessageAudience",
    "MessageId",
    "MessageLocalized",
    "MessageMark",
    "MessagePatch",
    "MessagePatchLocalized",
    "MessagePatchTemplate",
    "MessageTemplate",
    "MetadataCount",
    "ModelMetrics",
    "ModelMetricsOptions",
    "ModelsMetrics",
    "NamedAnnotationPlan",
    "NamedVector",
    "NamedVectorCreationMode",
    "NamedVectorProperties",
    "NewExperiment",
    "NewExperimentParameters",
    "NewGazetteer",
    "NewGazetteerParameters",
    "NewGroupDesc",
    "NewGroupDescMappingDiscriminator",
    "NewMessage",
    "NewMessageLocalized",
    "NewMessageTemplate",
    "NewNamedAnnotationPlan",
    "NewRole",
    "NewSuggester",
    "NewSuggesterParameters",
    "NewTheme",
    "NewUser",
    "OperationCount",
    "OutputParams",
    "OwnershipChange",
    "PartialLabel",
    "PartialLexicon",
    "PlanOperationResponse",
    "PlanPatch",
    "PlatformShare",
    "ProjectAnnotators",
    "ProjectBean",
    "ProjectConfigCreation",
    "ProjectConfigCreationProperties",
    "ProjectOpenSession",
    "ProjectOpenSessionState",
    "ProjectProperty",
    "ProjectsAnnotators",
    "ProjectStatus",
    "ProjectUserShare",
    "QualityFigures",
    "QuestionAnsweringParams",
    "QuestionAnsweringParamsLanguageDetection",
    "Report",
    "ReportClasses",
    "RequestJwtTokenProjectAccessMode",
    "RoleDesc",
    "RoleUpdate",
    "SearchDocumentsSearchType",
    "SearchFilter",
    "SearchFilterFilterSelector",
    "SearchFilterFilterType",
    "SearchParams",
    "SearchParamsType",
    "SearchRequest",
    "SearchSegmentsSearchType",
    "SearchTermsSearchType",
    "SearchTotal",
    "SearchTotalRelation",
    "Segment",
    "Segmenter",
    "SegmenterParameters",
    "SegmentHit",
    "SegmentHits",
    "SegmentMetadata",
    "SetThemeAsFavoriteScope",
    "ShareMode",
    "SherpaJobBean",
    "SherpaJobBeanStatus",
    "SherpaJobBeanType",
    "SigninAppBar",
    "SigninCardForm",
    "SigninCardMainTitles",
    "SigninCardSubtitles",
    "SigninConfig",
    "SigninFooter",
    "SimpleGroup",
    "SimpleGroupDesc",
    "SimpleGroupDescMappingDiscriminator",
    "SimpleGroupMembershipDesc",
    "SimpleMetadata",
    "SimpleUser",
    "Suggester",
    "SuggesterParameters",
    "SuggesterPatch",
    "SuggesterPatchParameters",
    "SuggestionFacets",
    "TermHit",
    "TermHits",
    "TermHitTerm",
    "TermIdentifier",
    "TermImport",
    "TermImporterSpec",
    "TermImporterSpecParameters",
    "TextCount",
    "Theme",
    "ThemeConfig",
    "ThemeId",
    "ThemeMedia",
    "ThemeUpdate",
    "UpdateThemeForm",
    "UploadedFile",
    "UploadedFileInfo",
    "UploadFilesBody",
    "UserGroupRef",
    "UserPermissionsUpdate",
    "UserProfile",
    "UserProfileUpdate",
    "UserResponse",
    "UserShare",
    "UsersResponse",
    "VectorParams",
    "VectorParamsNativeRRF",
    "VuetifyConfig",
    "VuetifyDarkTheme",
    "VuetifyLightTheme",
    "VuetifyThemes",
    "WithAnnotator",
    "WithAnnotatorCondition",
    "WithAnnotatorParameters",
    "WithConverter",
    "WithConverterCondition",
    "WithConverterParameters",
    "WithLanguageGuesser",
    "WithLanguageGuesserCondition",
    "WithLanguageGuesserParameters",
    "WithProcessor",
    "WithProcessorCondition",
    "WithProcessorParameters",
    "WithSegmenter",
    "WithSegmenterCondition",
    "WithSegmenterParameters",
    "WithVectorizer",
    "WithVectorizerCondition",
    "WithVectorizerParameters",
)
