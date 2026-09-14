"""Functions for selecting a diversified ETF allocation under constraints."""

from constants import (
    RETURN_POINTS_FACTOR,
    STABILITY_BENCHMARK,
    STABILITY_POINTS_FACTOR,
    DIVERSIFICATION_POINTS_FACTOR,
    EQUITIES_NEEDED,
    BONDS_NEEDED,
    GOLD_NEEDED,
    EQUITY,
    BOND,
    GOLD,
)


def get_etf_id(etf: str) -> str:
    """Return the three-character ETF identifier, or an empty string."""
    if etf == "":
        return ""
    return etf.split("_")[0]


def is_etf_available(etf: str, available_ids: str) -> bool:
    """Return whether the ETF is still available for selection."""
    if etf == "":
        return False
    return get_etf_id(etf) + "_" in available_ids


def get_asset_class(etf: str) -> str:
    """Return E, B, or G for equity, bond, or gold."""
    if etf == "":
        return ""
    return etf.split("_")[1][1]


def get_allocation(etf: str) -> int:
    """Return the proposed allocation percentage for the ETF."""
    if etf == "":
        return 0
    return int(etf.split("_")[-1][1:])


def get_expected_return(etf: str) -> int:
    """Return the illustrative annual return input as a percentage."""
    if etf == "":
        return 0
    return int(etf.split("_")[2][1:])


def get_volatility(etf: str) -> int:
    """Return the illustrative annual volatility input as a percentage."""
    if etf == "":
        return 0
    return int(etf.split("_")[3][1:])


def get_diversification(etf: str) -> int:
    """Return the illustrative diversification input from 0 to 100."""
    if etf == "":
        return 0
    return int(etf.split("_")[4][1:])


def can_select(etf: str, num_equities: int, num_bonds: int,
               num_gold: int) -> bool:
    """Return whether selecting the ETF stays within asset-class limits."""
    if etf == "":
        return True

    asset_class = get_asset_class(etf)
    if asset_class == EQUITY:
        return num_equities + 1 <= EQUITIES_NEEDED
    if asset_class == BOND:
        return num_bonds + 1 <= BONDS_NEEDED
    if asset_class == GOLD:
        return num_gold + 1 <= GOLD_NEEDED
    return False


def can_allocate(remaining_allocation: int, etf: str) -> bool:
    """Return whether the proposed ETF weight fits the remaining allocation."""
    return remaining_allocation >= get_allocation(etf)


def update_remaining_allocation(remaining_allocation: int, etf: str) -> int:
    """Return the remaining percentage after selecting the ETF."""
    if etf == "":
        return remaining_allocation
    return remaining_allocation - get_allocation(etf)


def add_to_portfolio(etf: str, selected_ids: str) -> str:
    """Return selected_ids with the ETF ID added once."""
    etf_id = get_etf_id(etf)
    if etf_id + "_" in selected_ids:
        return selected_ids
    return selected_ids + etf_id + "_"


def remove_etf(etf_ids: str, separator_index: int) -> str:
    """Remove the three-character ID ending at a valid separator index."""
    if etf_ids == "" or separator_index < 0 or separator_index >= len(etf_ids):
        return etf_ids
    if etf_ids[separator_index] != "_" or separator_index < 3:
        return etf_ids
    return etf_ids[:separator_index - 3] + etf_ids[separator_index + 1:]


def compute_return_points(etf: str) -> float:
    """Return points based on the illustrative return input."""
    return get_expected_return(etf) * RETURN_POINTS_FACTOR


def compute_stability_points(etf: str) -> float:
    """Return more points for volatility below the stability benchmark."""
    if etf == "":
        return 0.0
    difference = STABILITY_BENCHMARK - get_volatility(etf)
    return max(0, difference) * STABILITY_POINTS_FACTOR


def compute_diversification_points(etf: str) -> float:
    """Return points based on the illustrative diversification input."""
    return get_diversification(etf) * DIVERSIFICATION_POINTS_FACTOR


def compute_etf_score(etf: str) -> float:
    """Return the sum of return, stability, and diversification points."""
    if etf == "":
        return 0.0
    return (compute_return_points(etf)
            + compute_stability_points(etf)
            + compute_diversification_points(etf))
