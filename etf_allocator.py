"""Interactive portfolio builder for the risk-aware ETF allocation project."""

import csv

import etf_allocation_functions as af
from constants import (
    TOTAL_ALLOCATION,
    ETFS_TO_SELECT,
    EQUITIES_NEEDED,
    BONDS_NEEDED,
    GOLD_NEEDED,
    EQUITY,
    BOND,
)


def init_portfolio() -> dict:
    """Return a new empty portfolio dictionary."""
    return {
        "num_equities": 0,
        "num_bonds": 0,
        "num_gold": 0,
        "remaining_allocation": TOTAL_ALLOCATION,
        "selected_ids": "",
        "etfs": [],
    }


def etfs_selected(portfolio: dict) -> int:
    """Return the number of ETFs currently selected."""
    return (portfolio["num_equities"]
            + portfolio["num_bonds"]
            + portfolio["num_gold"])


def compute_portfolio_score(portfolio: dict) -> float:
    """Return the total score of all selected ETFs."""
    score = 0.0
    for etf in portfolio["etfs"]:
        score += af.compute_etf_score(etf)
    return score


def can_complete_portfolio(portfolio: dict, available_etfs: list[str]) -> bool:
    """Return whether the remaining required classes fit within the allocation."""
    equity_weights = sorted([
        af.get_allocation(etf) for etf in available_etfs
        if af.get_asset_class(etf) == EQUITY
    ])
    bond_weights = sorted([
        af.get_allocation(etf) for etf in available_etfs
        if af.get_asset_class(etf) == BOND
    ])
    gold_weights = sorted([
        af.get_allocation(etf) for etf in available_etfs
        if af.get_asset_class(etf) not in (EQUITY, BOND)
    ])

    equities_left = EQUITIES_NEEDED - portfolio["num_equities"]
    bonds_left = BONDS_NEEDED - portfolio["num_bonds"]
    gold_left = GOLD_NEEDED - portfolio["num_gold"]

    if (len(equity_weights) < equities_left
            or len(bond_weights) < bonds_left
            or len(gold_weights) < gold_left):
        return False

    minimum_needed = (
        sum(equity_weights[:equities_left])
        + sum(bond_weights[:bonds_left])
        + sum(gold_weights[:gold_left])
    )
    return minimum_needed <= portfolio["remaining_allocation"]


def select_etf(portfolio: dict, etf: str, available_etfs: list[str]) -> bool:
    """Select an ETF when class, allocation, and completion checks all pass."""
    portfolio_copy = portfolio.copy()
    available_copy = available_etfs.copy()
    available_copy.remove(etf)

    asset_class = af.get_asset_class(etf)
    if asset_class == EQUITY:
        portfolio_copy["num_equities"] += 1
    elif asset_class == BOND:
        portfolio_copy["num_bonds"] += 1
    else:
        portfolio_copy["num_gold"] += 1

    portfolio_copy["remaining_allocation"] = af.update_remaining_allocation(
        portfolio_copy["remaining_allocation"], etf
    )

    valid = (
        af.can_select(
            etf,
            portfolio["num_equities"],
            portfolio["num_bonds"],
            portfolio["num_gold"],
        )
        and af.can_allocate(portfolio["remaining_allocation"], etf)
        and can_complete_portfolio(portfolio_copy, available_copy)
    )

    if not valid:
        return False

    available_etfs.remove(etf)
    portfolio["selected_ids"] = af.add_to_portfolio(
        etf, portfolio["selected_ids"]
    )
    portfolio["remaining_allocation"] = af.update_remaining_allocation(
        portfolio["remaining_allocation"], etf
    )
    portfolio["etfs"].append(etf)

    if asset_class == EQUITY:
        portfolio["num_equities"] += 1
    elif asset_class == BOND:
        portfolio["num_bonds"] += 1
    else:
        portfolio["num_gold"] += 1
    return True


def load_etfs(path: str) -> tuple[list[str], dict[str, str]]:
    """Return encoded ETF records and their display names from a text file."""
    etfs = []
    names = {}
    with open(path, encoding="utf-8") as data_file:
        for line in data_file:
            if line.strip() == "":
                continue
            name, etf = line.strip().split(": ")
            etfs.append(etf)
            names[af.get_etf_id(etf)] = name
    return etfs, names


def export_portfolio(portfolio: dict, names: dict[str, str], path: str) -> None:
    """Write the selected portfolio to CSV for use in Excel."""
    with open(path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow([
            "ETF", "Name", "Asset Class", "Allocation %", "Expected Return %",
            "Volatility %", "Diversification Score", "ETF Score"
        ])
        for etf in portfolio["etfs"]:
            etf_id = af.get_etf_id(etf)
            writer.writerow([
                etf_id,
                names[etf_id],
                af.get_asset_class(etf),
                af.get_allocation(etf),
                af.get_expected_return(etf),
                af.get_volatility(etf),
                af.get_diversification(etf),
                af.compute_etf_score(etf),
            ])


def build_sample_portfolio(etfs: list[str]) -> dict:
    """Build the reproducible sample portfolio used in the Excel report."""
    portfolio = init_portfolio()
    selected_order = ["VFV", "XIC", "XEF", "XBB", "CGL"]
    for etf_id in selected_order:
        etf = next(item for item in etfs if af.get_etf_id(item) == etf_id)
        if not select_etf(portfolio, etf, etfs):
            raise ValueError("The sample portfolio could not satisfy its constraints.")
    return portfolio


def main() -> None:
    etfs, names = load_etfs("data/etfs.txt")
    portfolio = build_sample_portfolio(etfs)
    export_portfolio(portfolio, names, "output/selected_portfolio.csv")

    print("Selected ETFs:", portfolio["selected_ids"])
    print("Remaining allocation:", portfolio["remaining_allocation"], "%")
    print("Portfolio score:", compute_portfolio_score(portfolio))


if __name__ == "__main__":
    main()
