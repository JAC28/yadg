import pytest
from tests.utils import (
    datagram_from_input,
    standard_datagram_test,
    pars_datagram_test,
)


@pytest.mark.parametrize(
    "input, ts",
    [
        (
            {  # ts0 - rtf parser, supplied date
                "case": "Cp_100mA_1mindelay.rtf",
                "parameters": {"filetype": "drycal.rtf"},
                "externaldate": {"from": {"isostring": "2021-09-17"}},
            },
            {
                "nsteps": 1,
                "step": 0,
                "nrows": 110,
                "point": 0,
                "pars": {
                    "Temp": {"sigma": 0.1, "value": 27.4, "unit": "degC"},
                    "uts": {"value": 1631880613.0},
                },
            },
        ),
        (
            {  # ts1 - default sep parser, date from fn
                "case": "20211011_DryCal_out.csv",
                "parameters": {"filetype": "drycal.csv"},
                "externaldate": {"from": {"filename": {"format": "%Y%m%d", "len": 8}}},
            },
            {
                "nsteps": 1,
                "step": 0,
                "nrows": 29,
                "point": 0,
                "pars": {
                    "Temp": {"sigma": 0.1, "value": 24.3, "unit": "degC"},
                    "uts": {"value": 1633956333.0},
                },
            },
        ),
        (
            {  # ts2 - default sep parser, date from fn, sigma from length
                "case": "2021-10-11_DryCal_out.txt",
                "parameters": {"filetype": "drycal.txt"},
                "externaldate": {
                    "from": {"filename": {"format": "%Y-%m-%d", "len": 10}}
                },
            },
            {
                "nsteps": 1,
                "step": 0,
                "nrows": 29,
                "point": 28,
                "pars": {
                    "Pressure": {"sigma": 0.001, "value": 971.0, "unit": "mbar"},
                    "uts": {"value": 1633958360.0},
                },
            },
        ),
        (
            {  # ts3 - default sep parser, date from fn, calfile parser
                "case": "2021-10-11_DryCal_out.txt",
                "parameters": {"calfile": "drycal.json", "filetype": "drycal.txt"},
                "externaldate": {
                    "from": {"filename": {"format": "%Y-%m-%d", "len": 10}}
                },
            },
            {
                "nsteps": 1,
                "step": 0,
                "nrows": 29,
                "point": 28,
                "pars": {
                    "T": {"sigma": 0.1, "value": 299.25, "unit": "K", "raw": False},
                    "p": {"sigma": 100, "value": 97100.0, "unit": "Pa", "raw": False},
                },
            },
        ),
        (
            {  # ts4 - default sep parser, date from fn, passthrough units
                "case": "2021-10-11_DryCal_out.txt",
                "parameters": {"filetype": "drycal.txt"},
                "externaldate": {
                    "from": {"filename": {"format": "%Y-%m-%d", "len": 10}}
                },
            },
            {
                "nsteps": 1,
                "step": 0,
                "nrows": 29,
                "point": 28,
                "pars": {
                    "DryCal": {
                        "sigma": 0.0001,
                        "value": 14.848,
                        "unit": "smL/min",
                        "raw": True,
                    },
                },
            },
        ),
        (
            {  # ts5 - overnight run
                "case": "20220721-porosity-study-20p-Cu-200mA-EDLC-01-flow.csv",
                "parameters": {"filetype": "drycal.csv"},
                "externaldate": {"from": {"filename": {"format": "%Y%m%d", "len": 8}}},
            },
            {
                "nsteps": 1,
                "step": 0,
                "nrows": 77,
                "point": 76,
                "pars": {
                    "Temp": {"sigma": 0.1, "value": 28.6, "unit": "degC"},
                    "uts": {"value": 1658475079.0},
                },
            },
        ),
    ],
)
def test_datagram_from_drycal(input, ts, datadir):
    ret = datagram_from_input(input, "flowdata", datadir)
    standard_datagram_test(ret, ts)
    pars_datagram_test(ret, ts)
