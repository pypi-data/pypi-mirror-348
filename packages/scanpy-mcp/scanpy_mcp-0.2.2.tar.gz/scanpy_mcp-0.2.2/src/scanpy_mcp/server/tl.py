from fastmcp import FastMCP, Context
import os
import scanpy as sc
from ..schema.tl import *
from scmcp_shared.util import filter_args, add_op_log, forward_request
from scmcp_shared.logging_config import setup_logger
logger = setup_logger()

tl_mcp = FastMCP("ScanpyMCP-TL-Server")


@tl_mcp.tool()
async def tsne(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: TSNEModel = TSNEModel() 
):
    """t-distributed stochastic neighborhood embedding (t-SNE) for visualization"""

    try:
        result = await forward_request("tl_tsne", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.tl.tsne)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.tsne(adata, **func_kwargs)
        add_op_log(adata, sc.tl.tsne, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@tl_mcp.tool()
async def umap(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: UMAPModel = UMAPModel() 
):
    """Uniform Manifold Approximation and Projection (UMAP) for visualization"""

    try:
        result = await forward_request("tl_umap", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.tl.umap)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.umap(adata, **func_kwargs)
        add_op_log(adata, sc.tl.umap, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@tl_mcp.tool()
async def draw_graph(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: DrawGraphModel = DrawGraphModel() 
):
    """Force-directed graph drawing"""

    try:
        result = await forward_request("tl_draw_graph", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result    
        func_kwargs = filter_args(request, sc.tl.draw_graph)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.draw_graph(adata, **func_kwargs)
        add_op_log(adata, sc.tl.draw_graph, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@tl_mcp.tool()
async def diffmap(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: DiffMapModel = DiffMapModel() 
):
    """Diffusion Maps for dimensionality reduction"""

    try:
        result = await forward_request("tl_diffmap", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result    
        func_kwargs = filter_args(request, sc.tl.diffmap)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.diffmap(adata, **func_kwargs)
        adata.obsm["X_diffmap"] = adata.obsm["X_diffmap"][:,1:]
        add_op_log(adata, sc.tl.diffmap, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 

@tl_mcp.tool()
async def embedding_density(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: EmbeddingDensityModel = EmbeddingDensityModel() 
):
    """Calculate the density of cells in an embedding"""

    try:
        result = await forward_request("tl_embedding_density", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result        
        func_kwargs = filter_args(request, sc.tl.embedding_density)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.embedding_density(adata, **func_kwargs)
        add_op_log(adata, sc.tl.embedding_density, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 


@tl_mcp.tool()
async def leiden(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: LeidenModel = LeidenModel() 
):
    """Leiden clustering algorithm for community detection"""

    try:
        result = await forward_request("tl_leiden", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result            
        func_kwargs = filter_args(request, sc.tl.leiden)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.leiden(adata, **func_kwargs)
        add_op_log(adata, sc.tl.leiden, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@tl_mcp.tool()
async def louvain(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: LouvainModel = LouvainModel() 
):
    """Louvain clustering algorithm for community detection"""

    try:
        result = await forward_request("tl_louvain", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.tl.louvain)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.louvain(adata, **func_kwargs)
        add_op_log(adata, sc.tl.louvain, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@tl_mcp.tool()
async def dendrogram(
    ctx: Context,
    request: DendrogramModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
):
    """Hierarchical clustering dendrogram"""

    try:
        result = await forward_request("tl_dendrogram", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result        
        func_kwargs = filter_args(request, sc.tl.dendrogram)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.dendrogram(adata, **func_kwargs)
        add_op_log(adata, sc.tl.dendrogram, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 


@tl_mcp.tool()
async def dpt(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: DPTModel = DPTModel() 
):
    """Diffusion Pseudotime (DPT) analysis"""

    try:
        result = await forward_request("tl_dpt", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.tl.dpt)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.dpt(adata, **func_kwargs)
        add_op_log(adata, sc.tl.dpt, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 


@tl_mcp.tool()
async def paga(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: PAGAModel = PAGAModel() 
):
    """Partition-based graph abstraction"""

    try:
        result = await forward_request("tl_paga", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result         
        func_kwargs = filter_args(request, sc.tl.paga)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)    
        sc.tl.paga(adata, **func_kwargs)
        add_op_log(adata, sc.tl.paga, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 


@tl_mcp.tool()
async def ingest(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: IngestModel = IngestModel() 
):
    """Map labels and embeddings from reference data to new data"""

    try:
        result = await forward_request("tl_ingest", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result       
        func_kwargs = filter_args(request, sc.tl.ingest)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)    
        sc.tl.ingest(adata, **func_kwargs)
        add_op_log(adata, sc.tl.ingest, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 

@tl_mcp.tool()
async def rank_genes_groups(
    ctx: Context,
    request: RankGenesGroupsModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),

):
    """Rank genes for characterizing groups, for differentially expressison analysis"""

    try:
        result = await forward_request("tl_rank_genes_groups", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result         
        func_kwargs = filter_args(request, sc.tl.rank_genes_groups)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.rank_genes_groups(adata, **func_kwargs)
        add_op_log(adata, sc.tl.rank_genes_groups, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@tl_mcp.tool()
async def filter_rank_genes_groups(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: FilterRankGenesGroupsModel = FilterRankGenesGroupsModel() 
):
    """Filter out genes based on fold change and fraction of genes"""

    try:
        result = await forward_request("tl_filter_rank_genes_groups", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.tl.filter_rank_genes_groups)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.filter_rank_genes_groups(adata, **func_kwargs)
        add_op_log(adata, sc.tl.filter_rank_genes_groups, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 


@tl_mcp.tool()
async def marker_gene_overlap(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: MarkerGeneOverlapModel = MarkerGeneOverlapModel() 
):
    """Calculate overlap between data-derived marker genes and reference markers"""

    try:
        result = await forward_request("tl_marker_gene_overlap", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result         
        func_kwargs = filter_args(request, sc.tl.marker_gene_overlap)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.marker_gene_overlap(adata, **func_kwargs)
        add_op_log(adata, sc.tl.marker_gene_overlap, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 

@tl_mcp.tool()
async def score_genes(
    ctx: Context,
    request: ScoreGenesModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    
):
    """Score a set of genes based on their average expression"""
    try:
        result = await forward_request("tl_score_genes", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result       
        func_kwargs = filter_args(request, sc.tl.score_genes)
        ads = ctx.request_context.lifespan_context
        adata = ads.adata_dic[ads.active_id]
        sc.tl.score_genes(adata, **func_kwargs)
        add_op_log(adata, sc.tl.score_genes, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 

@tl_mcp.tool()
async def score_genes_cell_cycle(
    ctx: Context,
    request: ScoreGenesCellCycleModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    
):
    """Score cell cycle genes and assign cell cycle phases"""

    try:
        result = await forward_request("tl_score_genes_cell_cycle", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result       
        func_kwargs = filter_args(request, sc.tl.score_genes_cell_cycle)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.tl.score_genes_cell_cycle(adata, **func_kwargs)
        add_op_log(adata, sc.tl.score_genes_cell_cycle, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata},
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 