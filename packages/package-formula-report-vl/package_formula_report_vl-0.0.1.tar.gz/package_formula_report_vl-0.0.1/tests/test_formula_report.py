import pytest

from report import build_report

from report.cli import create_parser

@pytest.mark.parametrize('start_data, end_data, abb_data, expected_result', [
    ('DRR2018-05-24_12:11:24.067', 'DRR2018-05-24_12:14:12.054', 'DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER', 167.987)])
def test_formula_report_data(tmp_path, start_data, end_data, abb_data, expected_result):
    start_file = tmp_path / 'start.log'
    end_file = tmp_path / 'end.log'
    abb_file = tmp_path / 'abbreviations.txt'

    start_file.write_text(start_data)
    end_file.write_text(end_data)
    abb_file.write_text(abb_data)

    result = build_report(str(tmp_path))

    assert isinstance(result, list)
    assert result[0][0] == 'Daniel Ricciardo'
    assert result[0][1] == 'RED BULL RACING TAG HEUER'
    assert round(result[0][2], 3) == expected_result

@pytest.mark.parametrize('start_data, end_data, abb_data', [(
    ' ', ' ', 'DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER')])
def test_formula_report_empty_string(tmp_path, start_data, end_data, abb_data):
    start_file = tmp_path / 'start.log'
    end_file = tmp_path / 'end.log'
    abb_file = tmp_path / 'abbreviations.txt'

    start_file.write_text(start_data)
    end_file.write_text(end_data)
    abb_file.write_text(abb_data)

    with pytest.raises(TypeError):
        build_report(str(tmp_path))

@pytest.mark.parametrize('start_data, end_data, abb_data, expected_result', [(
    'DRR2018-05-24_12:14:12.054', 'DRR2018-05-24_12:11:24.067', 'DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER', 167.987)])
def test_formula_report_wrong_time(tmp_path, capsys, start_data, end_data, abb_data, expected_result):
    start_file = tmp_path / 'start.log'
    end_file = tmp_path / 'end.log'
    abb_file = tmp_path / 'abbreviations.txt'

    start_file.write_text(start_data)
    end_file.write_text(end_data)
    abb_file.write_text(abb_data)

    result = build_report(str(tmp_path))

    assert result == []

    captured = capsys.readouterr()
    assert 'The start time for DRR is later than the end time.' in captured.out

def test_cli():
    parser = create_parser()
    args = parser.parse_args(['--path', 'tests/data', '--order', 'asc'])
    assert args.path == 'tests/data'
    assert args.order == 'asc'
