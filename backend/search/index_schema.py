"""Create the policy search index: 1536-dim vectors, HNSW, semantic config."""
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField,
    VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration, HnswParameters,
    VectorSearchAlgorithmMetric, SemanticConfiguration, SemanticPrioritizedFields,
    SemanticField, SemanticSearch)
from config.settings import get_settings, credential


def build_index() -> SearchIndex:
    s = get_settings()
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String,
                        analyzer_name="en.microsoft"),
        SearchField(name="contentVector",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True,
                    vector_search_dimensions=s.embedding_dimensions,
                    vector_search_profile_name="hnsw-profile",
                    hidden=True),
        SearchableField(name="title", type=SearchFieldDataType.String,
                        filterable=True, facetable=True),
        SearchableField(name="section", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source_file", type=SearchFieldDataType.String,
                    filterable=True, facetable=True),
        SimpleField(name="page", type=SearchFieldDataType.Int32, filterable=True),
        SimpleField(name="chunk_index", type=SearchFieldDataType.Int32, filterable=True),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(
            name="hnsw-algo",
            parameters=HnswParameters(m=4, ef_construction=400, ef_search=500,
                                      metric=VectorSearchAlgorithmMetric.COSINE))],
        profiles=[VectorSearchProfile(name="hnsw-profile",
                                      algorithm_configuration_name="hnsw-algo")])

    semantic_search = SemanticSearch(configurations=[SemanticConfiguration(
        name="semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")],
            keywords_fields=[SemanticField(field_name="section")]))])

    return SearchIndex(name=s.search_index_name, fields=fields,
                       vector_search=vector_search, semantic_search=semantic_search)


def create():
    s = get_settings()
    client = SearchIndexClient(s.search_endpoint, credential())
    result = client.create_or_update_index(build_index())
    print(f"Index ready: {result.name}")
    print(f"  fields    : {len(result.fields)}")
    print(f"  vector dim: {s.embedding_dimensions}")
    print(f"  semantic  : {result.semantic_search.configurations[0].name}")
    return result


if __name__ == "__main__":
    create()
