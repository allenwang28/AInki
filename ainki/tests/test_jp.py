import pytest
from ainki.jp import example_processor


def test_tag_expression_1():
    expression = "飲む"
    sentence = "彼は毎日コーヒーを飲みます。"
    results = example_processor.tag_expression(
        sentence=sentence, expression=expression)
    assert results == "彼は毎日コーヒーを<span_id=\"expression\">飲み</span>ます。"


def test_tag_expression_2():
    expression = "走る"  # run
    sentence = "彼は昨日学校まで走ってきた。"  # He ran to the school yesterday.
    results = example_processor.tag_expression(
        sentence=sentence,
        expression=expression)
    assert results == "彼は昨日学校まで<span_id=\"expression\">走っ</span>てきた。"


def test_tag_expression_3():
    expression = "雨"  # rain
    sentence = "あめが降っているので、傘を持ってきました。"  # Since it's raining, I brought an umbrella.
    results = example_processor.tag_expression(
        sentence=sentence,
        expression=expression)
    assert results == "<span_id=\"expression\">あめ</span>が降っているので、傘を持ってきました。"
 

def test_tag_expression_4():
    expression = "山"  # mountain
    sentence = "富士山は日本の有名な火山です。"  # Mount Fuji is a famous volcano in Japan.
    results = example_processor.tag_expression(
        sentence=sentence,
        expression=expression)
    assert results == "富士<span_id=\"expression\">山</span>は日本の有名な火山です。"
 

def test_tag_expression_5():
    expression = "たべる"  # eat
    sentence = "私は寿司を食べたい。"  # I want to eat sushi.
    results = example_processor.tag_expression(
        sentence=sentence,
        expression=expression)
    assert results == "私は寿司を<span_id=\"expression\">食べ</span>たい。"
 

def test_process_1():
    expression = "飲む"
    sentence = "彼は毎日コーヒーを飲みます。"
    results = example_processor.process_sentence(
        sentence=sentence, expression=expression)
    assert results == "<ruby><rb>彼</rb><rt>かれ</rt></ruby>は<ruby><rb>毎日</rb><rt>まいにち</rt></ruby>コーヒーを<span_id=\"expression\"><ruby><rb>飲</rb><rt>の</rt></ruby>み</span>ます。"
 

def test_process_2():
    expression = "走る"  # run
    sentence = "彼は昨日学校まで走ってきた。"  # He ran to the school yesterday.
    results = example_processor.process_sentence(
        sentence=sentence, expression=expression)
    assert results == "<ruby><rb>彼</rb><rt>かれ</rt></ruby>は<ruby><rb>昨日</rb><rt>きのう</rt></ruby><ruby><rb>学校</rb><rt>がっこう</rt></ruby>まで<span_id=\"expression\"><ruby><rb>走</rb><rt>はし</rt></ruby>っ</span>てきた。"


def test_process_3():
    expression = "雨"  # rain
    sentence = "あめが降っているので、傘を持ってきました。"  # Since it's raining, I brought an umbrella.
    results = example_processor.process_sentence(
        sentence=sentence, expression=expression)
    assert results == "<span_id=\"expression\">あめ</span>が<ruby><rb>降</rb><rt>ふ</rt></ruby>っているので、<ruby><rb>傘</rb><rt>かさ</rt></ruby>を<ruby><rb>持</rb><rt>も</rt></ruby>ってきました。"


def test_process_4():
    expression = "山"  # mountain
    sentence = "富士山は日本の有名な火山です。"  # Mount Fuji is a famous volcano in Japan.
    results = example_processor.process_sentence(
        sentence=sentence, expression=expression)
    assert results == "<ruby><rb>富士</rb><rt>ふじ</rt></ruby><span_id=\"expression\"><ruby><rb>山</rb><rt>やま</rt></ruby></span>は<ruby><rb>日本</rb><rt>にっぽん</rt></ruby>の<ruby><rb>有名</rb><rt>ゆうめい</rt></ruby>な<ruby><rb>火山</rb><rt>かざん</rt></ruby>です。"


def test_process_5():
    expression = "たべる"  # eat
    sentence = "私は寿司を食べたい。"  # I want to eat sushi.
    results = example_processor.process_sentence(
        sentence=sentence, expression=expression)
    assert results == "<ruby><rb>私</rb><rt>わたし</rt></ruby>は<ruby><rb>寿司</rb><rt>すし</rt></ruby>を<span_id=\"expression\"><ruby><rb>食</rb><rt>た</rt></ruby>べ</span>たい。"