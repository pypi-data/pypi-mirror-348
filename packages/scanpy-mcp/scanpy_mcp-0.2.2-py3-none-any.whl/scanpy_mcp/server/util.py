import inspect
from fastmcp import FastMCP, Context
import os
import anndata as ad
from ..schema.util import *
from scmcp_shared.logging_config import setup_logger
from scmcp_shared.util import add_op_log,forward_request
logger = setup_logger()


ul_mcp = FastMCP("ScanpyMCP-Util-Server")


@ul_mcp.tool()
async def mark_var(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: MarkVarModel = MarkVarModel() 
):
    """
    Determine if each gene meets specific conditions and store results in adata.var as boolean values.
    For example: mitochondrion genes startswith MT-.
    The tool should be called first when calculate quality control metrics for mitochondrion, ribosomal, harhemoglobin genes, or other qc_vars.
    """
    try:
        result = await forward_request("ul_mark_var", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        var_name = request.var_name
        gene_class = request.gene_class
        pattern_type = request.pattern_type
        patterns = request.patterns
        if gene_class is not None:
            if gene_class == "mitochondrion":
                adata.var["mt"] = adata.var_names.str.startswith(('MT-', 'Mt','mt-'))
                var_name = "mt"
            elif gene_class == "ribosomal":
                adata.var["ribo"] = adata.var_names.str.startswith(("RPS", "RPL", "Rps", "Rpl"))
                var_name = "ribo"
            elif gene_class == "hemoglobin":
                adata.var["hb"] = adata.var_names.str.contains("^HB[^(P)]", case=False)
                var_name = "hb"    
        elif pattern_type is not None and patterns is not None:
            if pattern_type == "startswith":
                adata.var[var_name] = adata.var_names.str.startswith(patterns)
            elif pattern_type == "endswith":
                adata.var[var_name] = adata.var_names.str.endswith(patterns)
            elif pattern_type == "contains":
                adata.var[var_name] = adata.var_names.str.contains(patterns)
            else:
                raise ValueError(f"Did not support pattern_type: {pattern_type}")
        else:
            raise ValueError(f"Please provide validated parameter")
    
        res = {var_name: adata.var[var_name].value_counts().to_dict(), "msg": f"add '{var_name}' column in adata.var"}
        func_kwargs = {"var_name": var_name, "gene_class": gene_class, "pattern_type": pattern_type, "patterns": patterns}
        add_op_log(adata, "mark_var", func_kwargs)
        return res
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@ul_mcp.tool()
async def list_var(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: ListVarModel = ListVarModel() 
):
    """List key columns in adata.var. It should be called for checking when other tools need var key column names as input."""
    try:
        result = await forward_request("ul_list_var", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        columns = list(adata.var.columns)
        add_op_log(adata, list_var, {})
        return columns
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@ul_mcp.tool()
async def list_obs(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: ListObsModel = ListObsModel() 
):
    """List key columns in adata.obs. It should be called before other tools need obs key column names input."""
    try:
        result = await forward_request("ul_list_obs", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result    
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        columns = list(adata.obs.columns)
        add_op_log(adata, list_obs, {})
        return columns
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@ul_mcp.tool()
async def check_gene(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: VarNamesModel = VarNamesModel() 
):
    """Check if genes exist in adata.var_names. This tool should be called before gene expression visualizations or color by genes."""
    try:
        result = await forward_request("ul_check_gene", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result     
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        var_names = request.var_names
        result = {v: v in adata.var_names for v in var_names}
        add_op_log(adata, check_gene, {"var_names": var_names})
        return result
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@ul_mcp.tool()
async def merge_adata(
    ctx: Context,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    request: ConcatAdataModel = ConcatAdataModel() 
):
    """Merge multiple adata objects."""
     
    try:
        result = await forward_request("ul_merge_adata", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result
        ads = ctx.request_context.lifespan_context
        kwargs = {k: v for k, v in request.model_dump().items() if v is not None}
        merged_adata = ad.concat(list(ads.adata_dic[dtype].values()), **kwargs)
        ads.adata_dic[dtype] = {}
        ads.active_id = "merged_adata"
        add_op_log(merged_adata, ad.concat, kwargs)
        ads.adata_dic[ads.active_id] = merged_adata
        return {"status": "success", "message": "Successfully merged all AnnData objects"}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e


@ul_mcp.tool()
async def set_dpt_iroot(
    ctx: Context,
    request: DPTIROOTModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
    
):
    """Set the iroot cell"""
    try:
        result = await forward_request("ul_set_dpt_iroot", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result     
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        diffmap_key = request.diffmap_key
        dimension = request.dimension
        direction = request.direction
        if diffmap_key not in adata.obsm:
            raise ValueError(f"Diffusion map key '{diffmap_key}' not found in adata.obsm")
        if direction == "min":
            adata.uns["iroot"] = adata.obsm[diffmap_key][:, dimension].argmin()
        else:  
            adata.uns["iroot"] = adata.obsm[diffmap_key][:, dimension].argmax()
        
        func_kwargs = {"diffmap_key": diffmap_key, "dimension": dimension, "direction": direction}
        add_op_log(adata, "set_dpt_iroot", func_kwargs)
        
        return {"status": "success", "message": f"Successfully set root cell for DPT using {direction} of dimension {dimension}"}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@ul_mcp.tool()
async def add_layer(
    ctx: Context,
    request: AddLayerModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
):
    """Add a layer to the AnnData object.
    """
    try:
        result = await forward_request("ul_add_layer", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result         
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        layer_name = request.layer_name
        
        # Check if layer already exists
        if layer_name in adata.layers:
            raise ValueError(f"Layer '{layer_name}' already exists in adata.layers")
        # Add the data as a new layer
        adata.layers[layer_name] = adata.X.copy()

        func_kwargs = {"layer_name": layer_name}
        add_op_log(adata, "add_layer", func_kwargs)
        
        return {
            "status": "success", 
            "message": f"Successfully added layer '{layer_name}' to adata.layers"
        }
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@ul_mcp.tool()
async def map_cell_type(
    ctx: Context,
    request: CelltypeMapCellTypeModel,
    dtype: str = Field(default="exp", description="the datatype of anndata.X"),
    sampleid: str = Field(default=None, description="adata sampleid for analysis"),
):
    """Map cluster id to cell type names"""
    try:
        result = await forward_request("ul_map_cell_type", request, sampleid=sampleid, dtype=dtype)
        if result is not None:
            return result         
        ads = ctx.request_context.lifespan_context
        adata = ads.get_adata(dtype=dtype, sampleid=sampleid)
        cluster_key = request.cluster_key
        added_key = request.added_key

        if cluster_key not in adata.obs.columns:
            raise ValueError(f"cluster key '{cluster_key}' not found in adata.obs")
        if request.mapping is not None:
            adata.obs[added_key] = adata.obs[cluster_key].map(request.mapping)
        elif request.new_names is not None:
            adata.rename_categories(cluster_key, request.new_names)
        
        func_kwargs = {"cluster_key": cluster_key, "added_key": added_key, 
                    "mapping": request.mapping, "new_names": request.new_names}
        add_op_log(adata, "map_cell_type", func_kwargs)
        
        return {
            "status": "success", 
            "message": f"Successfully mapped values from '{cluster_key}' to '{added_key}'",
            "adata": adata
        }
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e

@ul_mcp.tool()
async def check_samples(ctx: Context):
    """check the stored samples    
    """
    try:
        ads = ctx.request_context.lifespan_context
        return {"sampleid": [list(ads.adata_dic[dk].keys()) for dk in ads.adata_dic.keys()]}
    except KeyError as e:
        raise e
    except Exception as e:
        if hasattr(e, '__context__') and e.__context__:
            raise Exception(f"{str(e.__context__)}")
        else:
            raise e