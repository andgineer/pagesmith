import pytest


@pytest.fixture(scope="function", params=["Hello 123 <br/> word/123 123-<word>\n<br/> and last!"])
def sentence_6_words(request):
    return request.param
