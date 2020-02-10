from turboshell.utils import extract_stubs


def test_extract_stubs():
    stubs = extract_stubs('p.show.all.new')
    assert stubs == ['p.', 'p.show.', 'p.show.all.']

    stubs = extract_stubs('p.show')
    assert stubs == ['p.']

    stubs = extract_stubs('no-dots')
    assert stubs == []