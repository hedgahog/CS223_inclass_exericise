from sort_and_search_funs import *
from util_funs import *
import anndata as ad


sort_times = {}  # algorithm label -> seconds, filled by the wrappers below


def record_time(label):
    """Like timer_decorator, but stores the elapsed time in sort_times for a final summary."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            sort_times[label] = time.perf_counter() - start
            return result
        return wrapper
    return decorator


# Timed wrappers give every algorithm the same `sort(arr)` signature.
@record_time("insertion (rec)")
def timed_insertion_sort_rec(arr):
    insertionSortRecursive(arr, len(arr))


@record_time("quick (rec)")
def timed_quick_sort_rec(arr):
    quick_sort_rec(arr, 0, len(arr) - 1)


@record_time("insertion (iter)")
def timed_insertion_sort_iter(arr):
    insertionSortIterative(arr)


@record_time("quick (iter)")
def timed_quick_sort_iter(arr):
    quick_sort_iter(arr)


def sort_adata_desc(adata, column, sort_func):
    """Return adata with rows reordered by `column`, largest first."""
    # Pair each value with its cell name so the row order can be recovered after sorting.
    pairs = list(zip(adata.obs[column], adata.obs_names))
    sort_func(pairs)
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

    adata_insert_rec = sort_adata_desc(adata_insert_rec, sort_column, timed_insertion_sort_rec)
    adata_quick_rec = sort_adata_desc(adata_quick_rec, sort_column, timed_quick_sort_rec)
    # TODO: selection / merge -- no recursive versions in sort_and_search_funs yet

    adata_insert_iter = adata.copy()
    adata_selection_iter = adata.copy()
    adata_merge_iter = adata.copy()
    adata_quick_iter = adata.copy()

    adata_insert_iter = sort_adata_desc(adata_insert_iter, sort_column, timed_insertion_sort_iter)
    adata_quick_iter = sort_adata_desc(adata_quick_iter, sort_column, timed_quick_sort_iter)
    # TODO: selection (iterative_selection_sort is unfinished) / merge (not written yet)




if __name__ == "__main__":
    adata = ad.read_h5ad("./data/pbmc_sample.h5ad")

    # Sanity checks: print intermediate results of the sorting step
    sort_column = adata.obs.columns[2]
    print(f"Loaded: {adata.n_obs} cells x {adata.n_vars} genes")
    print(f"Sort column: '{sort_column}'")
    print("Original (first 5):")
    print(adata.obs[sort_column].head())

    sorted_results = {
        "insertion (rec)": sort_adata_desc(adata, sort_column, timed_insertion_sort_rec),
        "quick (rec)": sort_adata_desc(adata, sort_column, timed_quick_sort_rec),
        "insertion (iter)": sort_adata_desc(adata, sort_column, timed_insertion_sort_iter),
        "quick (iter)": sort_adata_desc(adata, sort_column, timed_quick_sort_iter),
    }

    expected = sorted(adata.obs[sort_column], reverse=True)
    for name, sorted_adata in sorted_results.items():
        values = sorted_adata.obs[sort_column].tolist()
        print(f"\n[{name}] shape: {sorted_adata.shape}")
        print(f"[{name}] top 3: {values[:3]}, bottom 3: {values[-3:]}")
        print(f"[{name}] matches sorted(reverse=True): {values == expected}")

    print("\nOriginal adata unchanged:",
          adata.obs[sort_column].tolist() != expected)

    print(f"\nSorting time summary ({adata.n_obs} cells, fastest first):")
    for name, seconds in sorted(sort_times.items(), key=lambda item: item[1]):
        print(f"  {name:<16} {seconds:.6f} s")
