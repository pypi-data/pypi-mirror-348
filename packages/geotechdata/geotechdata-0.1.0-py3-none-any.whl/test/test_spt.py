import warnings
from geotechdata.borehole import SPTData

def test_blow_counts_calculation():
    # Case 1: blow_data has 3 values (no warning expected)
    spt = SPTData(depth=5.0, blow_data=[8, 10, 12])
    assert spt.blow_counts == 22  # 10 + 12

    # Case 2: blow_data has 2 values (warning expected)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        spt = SPTData(depth=6.0, blow_data=[7, 9])
        assert spt.blow_counts == 16  # 7 + 9
        assert any("less than 3 values" in str(warn.message) for warn in w)

    # Case 3: blow_data has 1 value (warning expected)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        spt = SPTData(depth=7.0, blow_data=[5])
        assert spt.blow_counts == 0  # less than 2 values
        assert any("less than 3 values" in str(warn.message) for warn in w)

    # Case 4: blow_data is None (no warning expected)
    spt = SPTData(depth=8.0)
    assert spt.blow_counts == 0

    # Case 5: blow_data is empty list (warning expected)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        spt = SPTData(depth=9.0, blow_data=[])
        assert spt.blow_counts == 0
        assert any("less than 3 values" in str(warn.message) for warn in w)

    # Case 6: blow_counts is provided directly (should take precedence, no warning)
    spt = SPTData(depth=10.0, blow_counts=15)
    assert spt.blow_counts == 15
    
def test_sptdata_user_defined_blow_counts():
    # Test that user-supplied blow_counts takes precedence over blow_data
    spt = SPTData(depth=11.0, blow_data=[1, 2, 3], blow_counts=99)
    assert spt.blow_counts == 99