import os
import inspect
from functools import partial
import scanpy as sc
from fastmcp import FastMCP, Context
from ..schema.pl import *
from pathlib import Path
from scmcp_shared.logging_config import setup_logger
from scmcp_shared.util import filter_args, set_fig_path, add_op_log,forward_request, obsm2adata

logger = setup_logger()

pl_mcp = FastMCP("ScanpyMCP-PL-Server")



@pl_mcp.tool()
async def pca(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    request: PCAModel = PCAModel() 
):
    """Scatter plot in PCA coordinates. default figure for PCA plot"""
    try:
        result = await forward_request("pl_pca", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)

        func_kwargs = filter_args(request, sc.pl.pca)
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        fig = sc.pl.pca(adata, **func_kwargs)
        fig_path = set_fig_path("pca", **func_kwargs)
        add_op_log(adata, sc.pl.pca, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 

@pl_mcp.tool()
async def diffmap(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    request: DiffusionMapModel = DiffusionMapModel() 
):
    """Plot diffusion map embedding of cells."""
    try:
        result = await forward_request("pl_diffmap", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result    
        func_kwargs = filter_args(request, sc.pl.diffmap)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
    
        fig = sc.pl.diffmap(adata, **func_kwargs)
        fig_path = set_fig_path("diffmap", **func_kwargs)
        add_op_log(adata, sc.pl.diffmap, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pl_mcp.tool()
async def violin(
    ctx: Context,
    request: ViolinModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
):
    """Plot violin plot of one or more variables."""
    try:
        result = await forward_request("pl_violin", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pl.violin)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        fig = sc.pl.violin(adata, **func_kwargs)
        fig_path = set_fig_path("violin", **func_kwargs)
        add_op_log(adata, sc.pl.violin, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def stacked_violin(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    request: StackedViolinModel = StackedViolinModel() 
):
    """Plot stacked violin plots. Makes a compact image composed of individual violin plots stacked on top of each other."""
    try:
        result = await forward_request("pl_stacked_violin", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result           
        func_kwargs = filter_args(request, sc.pl.stacked_violin)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
    
        fig = sc.pl.stacked_violin(adata, **func_kwargs)
        fig_path = set_fig_path("stacked_violin", **func_kwargs)
        add_op_log(adata, sc.pl.stacked_violin, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def heatmap(
    ctx: Context,
    request: HeatmapModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),

):
    """Heatmap of the expression values of genes."""
    try:
        result = await forward_request("pl_heatmap", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result           
        func_kwargs = filter_args(request, sc.pl.heatmap)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.heatmap(adata, **func_kwargs)
        fig_path = set_fig_path("heatmap", **func_kwargs)
        add_op_log(adata, sc.pl.heatmap, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def dotplot(
    ctx: Context,
    request: DotplotModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
):
    """Plot dot plot of expression values per gene for each group."""
    try:
        result = await forward_request("pl_dotplot", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result           
        func_kwargs = filter_args(request, sc.pl.dotplot)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.dotplot(adata, **func_kwargs)
        fig_path = set_fig_path("dotplot", **func_kwargs)
        add_op_log(adata, sc.pl.dotplot, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pl_mcp.tool()
async def matrixplot(
    ctx: Context,
    request: MatrixplotModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
):
    """matrixplot, Create a heatmap of the mean expression values per group of each var_names."""
    try:
        result = await forward_request("pl_matrixplot", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pl.matrixplot)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        if request.use_obsm is not None:
            adata = obsm2adata(adata, request.use_obsm)
        fig = sc.pl.matrixplot(adata, **func_kwargs)
        fig_path = set_fig_path("matrixplot", **func_kwargs)
        add_op_log(adata, sc.pl.matrixplot, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def tracksplot(
    ctx: Context,
    request: TracksplotModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
):
    """tracksplot, compact plot of expression of a list of genes."""
    try:
        result = await forward_request("pl_tracksplot", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pl.tracksplot)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.tracksplot(adata, **func_kwargs)
        fig_path = set_fig_path("tracksplot", **func_kwargs)
        add_op_log(adata, sc.pl.tracksplot, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pl_mcp.tool()
async def scatter(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    request: EnhancedScatterModel = EnhancedScatterModel() 
):
    """Plot a scatter plot of two variables, Scatter plot along observations or variables axes."""
    try:
        result = await forward_request("pl_scatter", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result    
        func_kwargs = filter_args(request, sc.pl.scatter)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.scatter(adata, **func_kwargs)
        fig_path = set_fig_path("scatter", **func_kwargs)
        add_op_log(adata, sc.pl.scatter, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pl_mcp.tool()
async def embedding(
    ctx: Context,
    request: EmbeddingModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    
):
    """Scatter plot for user specified embedding basis (e.g. umap, tsne, etc)."""
    try:
        result = await forward_request("pl_embedding", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result       
        func_kwargs = filter_args(request, sc.pl.embedding)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        try:      
            fig = sc.pl.embedding(adata, **func_kwargs)
        except KeyError as e:
            raise KeyError(f"Key '{e}' not found in adata.var and adata.obs. please check {e}, or {dtype}.")
        except Exception as e:
            raise e
        fig_path = set_fig_path("embedding", **func_kwargs)
        add_op_log(adata, sc.pl.embedding, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def embedding_density(
    ctx: Context,
    request: EmbeddingDensityModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
):
    """Plot the density of cells in an embedding."""
    try:
        result = await forward_request("pl_embedding_density", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.pl.embedding_density)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.embedding_density(adata, **func_kwargs)
        fig_path = set_fig_path("embedding_density", **func_kwargs)
        add_op_log(adata, sc.pl.embedding_density, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pl_mcp.tool()
async def rank_genes_groups(
    ctx: Context,
    request: RankGenesGroupsModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
):
    """Plot ranking of genes based on differential expression."""
    try:
        result = await forward_request("pl_rank_genes_groups", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result         
        func_kwargs = filter_args(request, sc.pl.rank_genes_groups)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.rank_genes_groups(adata, **func_kwargs)
        fig_path = set_fig_path("rank_genes_groups", **func_kwargs)
        add_op_log(adata, sc.pl.rank_genes_groups, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def rank_genes_groups_dotplot(
    ctx: Context,
    request: RankGenesGroupsDotplotModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
):
    """Plot ranking of genes(DEGs) using dotplot visualization. Defualt plot DEGs for rank_genes_groups tool"""
    try:
        result = await forward_request("pl_rank_genes_groups_dotplot", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pl.rank_genes_groups_dotplot)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.rank_genes_groups_dotplot(adata, **func_kwargs)
        fig_path = set_fig_path("rank_genes_groups_dotplot", **func_kwargs)
        add_op_log(adata, sc.pl.rank_genes_groups_dotplot, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def clustermap(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    request: ClusterMapModel = ClusterMapModel() 
):
    """Plot hierarchical clustering of cells and genes."""
    try:
        result = await forward_request("pl_clustermap", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pl.clustermap)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.clustermap(adata, **func_kwargs)
        fig_path = set_fig_path("clustermap", **func_kwargs)
        add_op_log(adata, sc.pl.clustermap, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pl_mcp.tool()
async def highly_variable_genes(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    request: HighlyVariableGenesModel = HighlyVariableGenesModel() 
):
    """plot highly variable genes; Plot dispersions or normalized variance versus means for genes."""
    try:
        result = await forward_request("pl_highly_variable_genes", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pl.highly_variable_genes)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
        
        fig = sc.pl.highly_variable_genes(adata, **func_kwargs)
        fig_path = set_fig_path("highly_variable_genes", **func_kwargs)
        add_op_log(adata, sc.pl.highly_variable_genes, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pl_mcp.tool()
async def pca_variance_ratio(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for plotting"),
    request: PCAVarianceRatioModel = PCAVarianceRatioModel() 
):
    """Plot the PCA variance ratio to visualize explained variance."""
    try:
        result = await forward_request("pl_pca_variance_ratio", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pl.pca_variance_ratio)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        
        func_kwargs.pop("return_fig", True)
        func_kwargs["show"] = False
        func_kwargs["save"] = ".png"
    
        fig = sc.pl.pca_variance_ratio(adata, **func_kwargs)
        fig_path = set_fig_path("pca_variance_ratio", **func_kwargs)
        add_op_log(adata, sc.pl.pca_variance_ratio, func_kwargs)
        return {"figpath": fig_path}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e
