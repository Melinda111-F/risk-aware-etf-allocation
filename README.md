# Risk-Aware ETF Portfolio Allocation Tool

This beginner-friendly project uses Python to build a diversified ETF allocation under simple asset-class and budget constraints. An Excel report then converts the selected percentage weights into a CAD 10,000 portfolio and applies an editable stress scenario.

The project was developed by adapting programming techniques from an introductory Python assignment: parsing encoded records, validating selections, updating a remaining budget, calculating component scores, and checking whether a valid final selection can still be completed.

## Project goal

The goal is to demonstrate how straightforward Python logic can support an explainable portfolio-allocation workflow without using advanced optimization or machine-learning models.

The sample moderate-risk portfolio contains:

| ETF | Asset class | Allocation |
| --- | --- | ---: |
| VFV | Equity | 25% |
| XIC | Equity | 20% |
| XEF | Equity | 15% |
| XBB | Bond | 30% |
| CGL | Gold | 10% |

## How it works

1. Read encoded ETF records from a text file.
2. Extract the ETF identifier, asset class, proposed weight, return input, volatility input, and diversification score.
3. Check asset-class limits and the remaining allocation before accepting an ETF.
4. Confirm that the remaining ETFs can still complete the required portfolio.
5. Calculate an explainable ETF score from return, stability, and diversification components.
6. Export the selected portfolio to CSV.
7. Use Excel formulas to calculate dollar allocations, category summaries, and a simple stress test.

## Stress-test example

The Excel workbook uses editable assumptions:

- Equity: -15%
- Bond: -3%
- Gold: +5%

Under this scenario, the CAD 10,000 sample portfolio falls to CAD 9,060, a change of -CAD 940.

## Files

- `etf_allocator.py` — portfolio construction, completion checks, and CSV export
- `etf_allocation_functions.py` — parsing, validation, allocation, and scoring functions
- `constants.py` — portfolio constraints and scoring constants
- `data/etfs.txt` — encoded illustrative ETF inputs
- `tests/test_etf_allocation.py` — unit tests for the core logic
- `output/selected_portfolio.csv` — reproducible sample output
- `output/Risk_Aware_ETF_Portfolio_Report.xlsx` — Excel analysis and stress-test report

## Run the project

```bash
python etf_allocator.py
python -m unittest discover -s tests -v
```

The Python portion uses only the standard library.

## Important note

All return, volatility, and diversification values are illustrative educational inputs. They are not market forecasts or investment advice.
