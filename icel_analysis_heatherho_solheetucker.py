from sort_and_search_funs import *
from util_funs import *
import anndata as ad
import csv


sort_times = {}  # algorithm label -> (seconds, n_cells sorted), filled by the wrappers below


def record_time(label):
    """Like timer_decorator, but stores the elapsed time in sort_times for a final summary."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(arr, *args, **kwargs):
            n = len(arr)
            start = time.perf_counter()
            result = func(arr, *args, **kwargs)
            sort_times[label] = (time.perf_counter() - start, n)
            return result
        return wrapper
    return decorator


# Timed wrappers give every algorithm the same `sort(arr)` signature.
@record_time("insertion (rec)")
def timed_insertion_sort_rec(arr):
    insertionSortRecursive(arr, len(arr))


@record_time("selection (rec)")
def timed_selection_sort_rec(arr):
    recursive_selection_sort(arr, 0, len(arr))


@record_time("merge (rec)")
def timed_merge_sort_rec(arr):
    merge_sort_rec(arr, 0, len(arr) - 1)


@record_time("quick (rec)")
def timed_quick_sort_rec(arr):
    quick_sort_rec(arr, 0, len(arr) - 1)


@record_time("insertion (iter)")
def timed_insertion_sort_iter(arr):
    insertionSortIterative(arr)


@record_time("selection (iter)")
def timed_selection_sort_iter(arr):
    iterative_selection_sort(arr)


@record_time("merge (iter)")
def timed_merge_sort_iter(arr):
    merge_sort_iter(arr)


@record_time("quick (iter)")
def timed_quick_sort_iter(arr):
    quick_sort_iter(arr)


# Second set of timed wrappers, used for the Col 2 (genes expressed) sort in
# filter_mt_cells, so those timings land under their own labels instead of
# overwriting the Col 3 (percent_mito) timings recorded above.
@record_time("insertion (rec) - genes")
def timed_insertion_sort_rec_genes(arr):
    insertionSortRecursive(arr, len(arr))


@record_time("selection (rec) - genes")
def timed_selection_sort_rec_genes(arr):
    recursive_selection_sort(arr, 0, len(arr))


@record_time("merge (rec) - genes")
def timed_merge_sort_rec_genes(arr):
    merge_sort_rec(arr, 0, len(arr) - 1)


@record_time("quick (rec) - genes")
def timed_quick_sort_rec_genes(arr):
    quick_sort_rec(arr, 0, len(arr) - 1)


@record_time("insertion (iter) - genes")
def timed_insertion_sort_iter_genes(arr):
    insertionSortIterative(arr)


@record_time("selection (iter) - genes")
def timed_selection_sort_iter_genes(arr):
    iterative_selection_sort(arr)


@record_time("merge (iter) - genes")
def timed_merge_sort_iter_genes(arr):
    merge_sort_iter(arr)


@record_time("quick (iter) - genes")
def timed_quick_sort_iter_genes(arr):
    quick_sort_iter(arr)


def sort_adata(adata, column, sort_func, descending=True):
    """Return adata with rows reordered by `column`, largest first."""
    # Pair each value with its cell name so the row order can be recovered after sorting.
    pairs = list(zip(adata.obs[column], adata.obs_names))
    sort_func(pairs)
    if descending:
        pairs.reverse()  # sort functions are ascending
    sorted_cell_names = [name for _, name in pairs]
    return adata[sorted_cell_names].copy()


def filter_mt_cells(adata, mt_exp_lvl_threshold, gene_exp_threshold):
    if not 0 <= mt_exp_lvl_threshold <= 1:
        raise ValueError("mt_exp_lvl_threshold must be between 0 and 1")
    if not 0<= gene_exp_threshold <= 2000 :
        raise ValueError("gene_exp_threshold must be between 0 and 2000")

    # adata_insert_rec = copy adata to avoid modifying the original adata
    adata_insert_rec = adata.copy()
    adata_selection_rec = adata.copy()
    adata_merge_rec = adata.copy()
    adata_quick_rec = adata.copy()

    # Sort tables by 3rd column, descending order, using different sorting algorithms, time with util_funs.
    sort_column = adata.obs.columns[2]  # 'percent_mito'

    adata_insert_rec = sort_adata(adata_insert_rec, sort_column, timed_insertion_sort_rec, descending=True)
    adata_selection_rec = sort_adata(adata_selection_rec, sort_column, timed_selection_sort_rec, descending=True)
    adata_merge_rec = sort_adata(adata_merge_rec, sort_column, timed_merge_sort_rec, descending=True)
    adata_quick_rec = sort_adata(adata_quick_rec, sort_column, timed_quick_sort_rec, descending=True)

    adata_insert_iter = adata.copy()
    adata_selection_iter = adata.copy()
    adata_merge_iter = adata.copy()
    adata_quick_iter = adata.copy()

    adata_insert_iter = sort_adata(adata_insert_iter, sort_column, timed_insertion_sort_iter, descending=True)
    adata_selection_iter = sort_adata(adata_selection_iter, sort_column, timed_selection_sort_iter, descending=True)
    adata_merge_iter = sort_adata(adata_merge_iter, sort_column, timed_merge_sort_iter, descending=True)
    adata_quick_iter = sort_adata(adata_quick_iter, sort_column, timed_quick_sort_iter, descending=True)
    #--------Heather--------
    # 7c
    # from each sorted dataframe, create new dataframe that
    # doesn't contain a cell row entry if value in col 3 is greater than 
    # mt_exp_lvl_threshold
    # adata_filtered = filter col3 greater than mt_ecp_lvl_threshold

    # recursive
    af_insert_rec = adata_insert_rec[adata_insert_rec.obs[sort_column] <= mt_exp_lvl_threshold].copy()
    af_selection_rec = adata_selection_rec[adata_selection_rec.obs[sort_column] <= mt_exp_lvl_threshold].copy()
    af_merge_rec = adata_merge_rec[adata_merge_rec.obs[sort_column] <= mt_exp_lvl_threshold].copy()
    af_quick_rec = adata_quick_rec[adata_quick_rec.obs[sort_column] <= mt_exp_lvl_threshold].copy()

    # iterative
    af_insert_iter = adata_insert_iter[adata_insert_iter.obs[sort_column] <= mt_exp_lvl_threshold].copy()
    af_selection_iter = adata_selection_iter[adata_selection_iter.obs[sort_column] <= mt_exp_lvl_threshold].copy()
    af_merge_iter = adata_merge_iter[adata_merge_iter.obs[sort_column] <= mt_exp_lvl_threshold].copy()
    af_quick_iter = adata_quick_iter[adata_quick_iter.obs[sort_column] <= mt_exp_lvl_threshold].copy()  

    
    # 7d: take the mito-filtered results from 7c and sort them by column 2
    # (genes expressed), ascending order, timing each algorithm again.
    gene_column = adata.obs.columns[1]  # 'n_genes_by_counts'
    # ascending order, so don't reverse after sorting
    gf_insert_rec = sort_adata(af_insert_rec, gene_column, timed_insertion_sort_rec_genes, descending=False)
    gf_selection_rec = sort_adata(af_selection_rec, gene_column, timed_selection_sort_rec_genes, descending=False)
    gf_merge_rec = sort_adata(af_merge_rec, gene_column, timed_merge_sort_rec_genes, descending=False)
    gf_quick_rec = sort_adata(af_quick_rec, gene_column, timed_quick_sort_rec_genes, descending=False)

    gf_insert_iter = sort_adata(af_insert_iter, gene_column, timed_insertion_sort_iter_genes, descending=False)
    gf_selection_iter = sort_adata(af_selection_iter, gene_column, timed_selection_sort_iter_genes, descending=False)
    gf_merge_iter = sort_adata(af_merge_iter, gene_column, timed_merge_sort_iter_genes, descending=False)
    gf_quick_iter = sort_adata(af_quick_iter, gene_column, timed_quick_sort_iter_genes, descending=False)

    # Remove cells whose gene count is below gene_exp_threshold.
    gf_insert_rec_filtered = gf_insert_rec[gf_insert_rec.obs[gene_column] >= gene_exp_threshold].copy()
    gf_selection_rec_filtered = gf_selection_rec[gf_selection_rec.obs[gene_column] >= gene_exp_threshold].copy()
    gf_merge_rec_filtered = gf_merge_rec[gf_merge_rec.obs[gene_column] >= gene_exp_threshold].copy()
    gf_quick_rec_filtered = gf_quick_rec[gf_quick_rec.obs[gene_column] >= gene_exp_threshold].copy()
    gf_insert_iter_filtered = gf_insert_iter[gf_insert_iter.obs[gene_column] >= gene_exp_threshold].copy()
    gf_selection_iter_filtered = gf_selection_iter[gf_selection_iter.obs[gene_column] >= gene_exp_threshold].copy()
    gf_merge_iter_filtered = gf_merge_iter[gf_merge_iter.obs[gene_column] >= gene_exp_threshold].copy()
    gf_quick_iter_filtered = gf_quick_iter[gf_quick_iter.obs[gene_column] >= gene_exp_threshold].copy()

    return {
        "insertion (rec)": gf_insert_rec_filtered,
        "selection (rec)": gf_selection_rec_filtered,
        "merge (rec)": gf_merge_rec_filtered,
        "quick (rec)": gf_quick_rec_filtered,
        "insertion (iter)": gf_insert_iter_filtered,
        "selection (iter)": gf_selection_iter_filtered,
        "merge (iter)": gf_merge_iter_filtered,
        "quick (iter)": gf_quick_iter_filtered,
    }


if __name__ == "__main__":
    adata = ad.read_h5ad("./data/pbmc_sample.h5ad")

    # Sanity checks: print intermediate results of the sorting step
    sort_column = adata.obs.columns[2]
    print(f"Loaded: {adata.n_obs} cells x {adata.n_vars} genes")
    print(f"Sort column: '{sort_column}'")
    print("Original (first 5):")
    print(adata.obs[sort_column].head())

    sorted_results = {
        "insertion (rec)": sort_adata(adata, sort_column, timed_insertion_sort_rec, descending=True),
        "selection (rec)": sort_adata(adata, sort_column, timed_selection_sort_rec, descending=True),
        "merge (rec)": sort_adata(adata, sort_column, timed_merge_sort_rec, descending=True),
        "quick (rec)": sort_adata(adata, sort_column, timed_quick_sort_rec, descending=True),
        "insertion (iter)": sort_adata(adata, sort_column, timed_insertion_sort_iter, descending=True),
        "selection (iter)": sort_adata(adata, sort_column, timed_selection_sort_iter, descending=True),
        "merge (iter)": sort_adata(adata, sort_column, timed_merge_sort_iter, descending=True),
        "quick (iter)": sort_adata(adata, sort_column, timed_quick_sort_iter, descending=True),
    }

    expected = sorted(adata.obs[sort_column], reverse=True)
    for name, sorted_adata in sorted_results.items():
        values = sorted_adata.obs[sort_column].tolist()
        print(f"\n[{name}] shape: {sorted_adata.shape}")
        print(f"[{name}] top 3: {values[:3]}, bottom 3: {values[-3:]}")
        print(f"[{name}] matches sorted(reverse=True): {values == expected}")

    print("\nOriginal adata unchanged:",
          adata.obs[sort_column].tolist() != expected)

    # Run the full mito + gene-expression filtering pipeline (7b-7d) and
    # report the resulting cell counts for each algorithm variant.
    mt_exp_lvl_threshold = 0.02
    gene_exp_threshold = 500
    filtered_results = filter_mt_cells(adata, mt_exp_lvl_threshold, gene_exp_threshold)
    print(f"\nfilter_mt_cells(mt <= {mt_exp_lvl_threshold}, genes >= {gene_exp_threshold}):")
    for name, filtered_adata in filtered_results.items():
        print(f"[{name}] shape: {filtered_adata.shape}")

    def split_label(label):
        """Split a sort_times label into (algorithm, stage, filtered), e.g.
        "insertion (rec) - genes" -> ("insertion (rec)", "genes_expressed", "filtered")."""
        if label.endswith(" - genes"):
            return label[: -len(" - genes")], "genes_expressed", "filtered"
        return label, "percent_mito", "unfiltered"

    with open("sort_times.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "stage", "filtered", "n_cells", "seconds"])
        rows = [(*split_label(name), n, seconds) for name, (seconds, n) in sort_times.items()]
        for algorithm, stage, filtered, n, seconds in sorted(rows, key=lambda row: (row[0], row[1])):
            writer.writerow([algorithm, stage, filtered, n, f"{seconds:.6f}"])
