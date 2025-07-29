
import os
import inspect
import scanpy as sc
from fastmcp import FastMCP , Context
from ..schema.pp import *
from scmcp_shared.util import filter_args, add_op_log, forward_request
from scmcp_shared.logging_config import setup_logger
logger = setup_logger()


pp_mcp = FastMCP("ScanpyMCP-PP-Server")


@pp_mcp.tool()
async def subset_cells(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: SubsetCellModel = SubsetCellModel() 
):
    """filter or subset cells based on total genes expressed counts and numbers. or values in adata.obs[obs_key]"""

    try:
        result = await forward_request("subset_cells", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result

        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid).copy()
        func_kwargs = filter_args(request, sc.pp.filter_cells)
        if func_kwargs:
            sc.pp.filter_cells(adata, **func_kwargs)
            add_op_log(adata, sc.pp.filter_cells, func_kwargs)
        # Subset based on obs (cells) criteria
        if request.obs_key is not None:
            if request.obs_key not in adata.obs.columns:
                raise ValueError(f"Key '{request.obs_key}' not found in adata.obs")        
            mask = True  # Start with all cells selected
            if request.obs_value is not None:
                mask = mask & (adata.obs[request.obs_key] == request.obs_value)
            if request.obs_min is not None:
                mask = mask & (adata.obs[request.obs_key] >= request.obs_min)        
            if request.obs_max is not None:
                mask = mask & (adata.obs[request.obs_key] <= request.obs_max)        
            adata = adata[mask, :]
            add_op_log(adata, "subset_cells", 
                {
                "obs_key": request.obs_key, "obs_value": request.obs_value, 
                "obs_min": request.obs_min, "obs_max": request.obs_max
                }
            )
        ads.set_adata(adata, sampleid=sampleid, sdtype=dtype)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pp_mcp.tool()
async def subset_genes(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: SubsetGeneModel = SubsetGeneModel() 
):
    """filter or subset genes based on number of cells or counts, or values in adata.var[var_key] or subset highly variable genes""" 
    try:
        result = await forward_request("pp_subset_genes", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pp.filter_genes)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid).copy()
        if func_kwargs:
            sc.pp.filter_genes(adata, **func_kwargs)
            add_op_log(adata, sc.pp.filter_genes, func_kwargs)
        if request.var_key is not None:
            if request.var_key not in adata.var.columns:
                raise ValueError(f"Key '{request.var_key}' not found in adata.var")
            mask = True  # Start with all genes selected
            if request.var_min is not None:
                mask = mask & (adata.var[request.var_key] >= request.var_min)
            if request.var_max is not None:
                mask = mask & (adata.var[request.var_key] <= request.var_max)        
            adata = adata[:, mask]
            if request.highly_variable is not None:
                adata = adata[:, adata.var.highly_variable]
            add_op_log(adata, "subset_genes", 
                {
                "var_key": request.var_key, "var_value": request.var_value, 
                "var_min": request.var_min, "var_max": request.var_max, "hpv":  request.highly_variable
                }
            )
        ads.set_adata(adata, sampleid=sampleid, sdtype=dtype)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pp_mcp.tool()
async def calculate_qc_metrics(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: CalculateQCMetrics = CalculateQCMetrics() 
):
    """Calculate quality control metrics(common metrics: total counts, gene number, percentage of counts in ribosomal and mitochondrial) for AnnData."""

    try:
        result = await forward_request("pp_calculate_qc_metrics", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        logger.info(f"calculate_qc_metrics {request.model_dump()}")
        func_kwargs = filter_args(request, sc.pp.calculate_qc_metrics)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        func_kwargs["inplace"] = True
        try:
            sc.pp.calculate_qc_metrics(adata, **func_kwargs)
            add_op_log(adata, sc.pp.calculate_qc_metrics, func_kwargs)
        except KeyError as e:
            raise KeyError(f"Cound find {e} in adata.var")
        return [
                {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
            ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 


@pp_mcp.tool()
async def log1p(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: Log1PModel = Log1PModel() 
):
    """Logarithmize the data matrix (X = log(X + 1))"""

    try:
        result = await forward_request("pp_log1p", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pp.log1p)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid).copy()
        try:
            sc.pp.log1p(adata, **func_kwargs)
            adata.raw = adata.copy()
            add_op_log(adata, sc.pp.log1p, func_kwargs)
        except Exception as e:
            raise e
        ads.set_adata(adata, sampleid=sampleid, sdtype=dtype)
        return [
                {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
            ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pp_mcp.tool()
async def normalize_total(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: NormalizeTotalModel = NormalizeTotalModel() 
):
    """Normalize counts per cell to the same total count"""

    try:
        result = await forward_request("pp_normalize_total", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pp.normalize_total)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid).copy()
        sc.pp.normalize_total(adata, **func_kwargs)
        add_op_log(adata, sc.pp.normalize_total, func_kwargs)
        ads.set_adata(adata, sampleid=sampleid, sdtype=dtype)
        return [
                {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
            ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@pp_mcp.tool()
async def pca(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: PCAModel = PCAModel() 
):
    """Principal component analysis"""

    try:
        result = await forward_request("pp_pca", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pp.pca)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.pp.pca(adata, **func_kwargs)
        add_op_log(adata, sc.pp.pca, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pp_mcp.tool()
async def highly_variable_genes(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: HighlyVariableGenesModel = HighlyVariableGenesModel() 
):
    """Annotate highly variable genes"""

    try:
        result = await forward_request("pp_highly_variable_genes", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        try:  
            func_kwargs = filter_args(request, sc.pp.highly_variable_genes)
            ads = ctx.request_context.lifespan_context
            adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
            sc.pp.highly_variable_genes(adata, **func_kwargs)
            add_op_log(adata, sc.pp.highly_variable_genes, func_kwargs)
        except Exception as e:
            logger.error(f"Error in pp_highly_variable_genes: {str(e)}")
            raise e
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e
@pp_mcp.tool()
async def regress_out(
    ctx: Context,
    request: RegressOutModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    
):
    """Regress out (mostly) unwanted sources of variation."""

    try:
        result = await forward_request("pp_regress_out", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result        
        func_kwargs = filter_args(request, sc.pp.regress_out)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid).copy()

        sc.pp.regress_out(adata, **func_kwargs)
        add_op_log(adata, sc.pp.regress_out, func_kwargs)

        ads.set_adata(adata, sampleid=sampleid, sdtype=dtype)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pp_mcp.tool()
async def scale(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: ScaleModel = ScaleModel() 
):
    """Scale data to unit variance and zero mean"""

    try:
        result = await forward_request("pp_scale", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result     
        func_kwargs = filter_args(request, sc.pp.scale)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid).copy()

        sc.pp.scale(adata, **func_kwargs)
        add_op_log(adata, sc.pp.scale, func_kwargs)
 
        ads.set_adata(adata, sampleid=sampleid, sdtype=dtype)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pp_mcp.tool()
async def combat(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: CombatModel = CombatModel() 
):
    """ComBat function for batch effect correction"""

    try:
        result = await forward_request("pp_combat", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result        
        func_kwargs = filter_args(request, sc.pp.combat)
        ads = ctx.request_context.lifespan_context
        adata = ads.adata_dic[ads.active_id].copy()

        sc.pp.combat(adata, **func_kwargs)
        add_op_log(adata, sc.pp.combat, func_kwargs)

        ads.set_adata(adata, sampleid=sampleid, sdtype=dtype)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@pp_mcp.tool()
async def scrublet(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: ScrubletModel = ScrubletModel() 
):
    """Predict doublets using Scrublet"""

    try:
        result = await forward_request("pp_scrublet", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result          
        func_kwargs = filter_args(request, sc.pp.scrublet)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.pp.scrublet(adata, **func_kwargs)
        add_op_log(adata, sc.pp.scrublet, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e 

@pp_mcp.tool()
async def neighbors(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for preprocessing"),
    request: NeighborsModel = NeighborsModel() 
):
    """Compute nearest neighbors distance matrix and neighborhood graph"""

    try:
        result = await forward_request("pp_neighbors", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        func_kwargs = filter_args(request, sc.pp.neighbors)
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        sc.pp.neighbors(adata, **func_kwargs)
        add_op_log(adata, sc.pp.neighbors, func_kwargs)
        return [
            {"sampleid": sampleid or ads.active_id, "dtype": dtype, "adata": adata}
        ]
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e