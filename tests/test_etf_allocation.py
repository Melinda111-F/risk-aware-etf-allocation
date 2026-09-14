"""Unit tests for the ETF allocation functions and portfolio constraints."""

import unittest

import etf_allocation_functions as af
from etf_allocator import (
    build_sample_portfolio,
    can_complete_portfolio,
    compute_portfolio_score,
    init_portfolio,
    load_etfs,
    select_etf,
)


SAMPLE_EQUITY = "VFV_AE_R12_V18_D80_W25"
SAMPLE_BOND = "XBB_AB_R4_V7_D70_W30"


class TestAllocationFunctions(unittest.TestCase):
    def test_parse_etf_fields(self) -> None:
        self.assertEqual(af.get_etf_id(SAMPLE_EQUITY), "VFV")
        self.assertEqual(af.get_asset_class(SAMPLE_EQUITY), "E")
        self.assertEqual(af.get_allocation(SAMPLE_EQUITY), 25)

    def test_availability(self) -> None:
        self.assertTrue(af.is_etf_available(SAMPLE_EQUITY, "VFV_XBB_"))
        self.assertFalse(af.is_etf_available("XIC_AE_R8_V16_D75_W20", "VFV_XBB_"))

    def test_allocation_update(self) -> None:
        self.assertTrue(af.can_allocate(30, SAMPLE_EQUITY))
        self.assertEqual(af.update_remaining_allocation(30, SAMPLE_EQUITY), 5)

    def test_asset_class_limit(self) -> None:
        self.assertFalse(af.can_select(SAMPLE_EQUITY, 3, 0, 0))
        self.assertTrue(af.can_select(SAMPLE_BOND, 3, 0, 0))

    def test_score_is_sum_of_components(self) -> None:
        expected = (
            af.compute_return_points(SAMPLE_EQUITY)
            + af.compute_stability_points(SAMPLE_EQUITY)
            + af.compute_diversification_points(SAMPLE_EQUITY)
        )
        self.assertEqual(af.compute_etf_score(SAMPLE_EQUITY), expected)

    def test_sample_portfolio_meets_constraints(self) -> None:
        etfs, unused_names = load_etfs("data/etfs.txt")
        portfolio = build_sample_portfolio(etfs)
        self.assertEqual(portfolio["num_equities"], 3)
        self.assertEqual(portfolio["num_bonds"], 1)
        self.assertEqual(portfolio["num_gold"], 1)
        self.assertEqual(portfolio["remaining_allocation"], 0)
        self.assertGreater(compute_portfolio_score(portfolio), 0)

    def test_rejects_fourth_equity(self) -> None:
        etfs, unused_names = load_etfs("data/etfs.txt")
        portfolio = init_portfolio()
        equities = [etf for etf in etfs if af.get_asset_class(etf) == "E"]
        self.assertTrue(select_etf(portfolio, equities[0], etfs))
        self.assertTrue(select_etf(portfolio, equities[1], etfs))
        self.assertTrue(select_etf(portfolio, equities[2], etfs))
        self.assertFalse(select_etf(portfolio, equities[3], etfs))

    def test_can_complete_portfolio_checks_remaining_classes(self) -> None:
        portfolio = init_portfolio()
        self.assertFalse(can_complete_portfolio(portfolio, [SAMPLE_EQUITY]))


if __name__ == "__main__":
    unittest.main()
