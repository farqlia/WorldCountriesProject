import src.web_scraping.destructuring as destructuring

test_case_1 = '''
<p>
    <strong>0-14 years: </strong>
    39.8% (male 7,926,748/female 7,686,979)
    <br>
    <br>
    <strong>15-64 years: </strong>
    57.35% (male 11,413,654/female 11,084,665)
    <br>
    <br>
    <strong>65 years and over: </strong>
    2.85% (2023 est.) (male 515,147/female 604,810)
</p>
    '''

class TestDestructureListLikeParagraph:


    def test_for_destructure(self):

        expected = {"0-14 years": "39.8% (male 7,926,748/female 7,686,979)",
                    "15-64 years": "57.35% (male 11,413,654/female 11,084,665)",
                    "65 years and over": "2.85% (2023 est.) (male 515,147/female 604,810)"}
        assert expected == destructuring.destructure_list_like(test_case_1)


test_case_2 = '''
<p>
    7.893 million metric tonnes of CO2 (2019 est.)
    <br>
    <br>
    <strong>
    from coal and metallurgical coke: </strong>
    4.158 million metric tonnes of CO2 (2019 est.)
    <br>
    <br>
    <strong>from petroleum and other liquids: </strong>
    3.468 million metric tonnes of CO2 (2019 est.)
    <br>
    <br>
    <strong>from consumed natural gas: </strong>
    267,000 metric tonnes of CO2 (2019 est.)
</p>
'''

class TestDestructureListLikeParagraphWithCaption:

    def test_for_destructure(self):

        expected = {"from coal and metallurgical coke": "4.158 million metric tonnes of CO2 (2019 est.)",
                    "from petroleum and other liquids": "3.468 million metric tonnes of CO2 (2019 est.)",
                    "from consumed natural gas": "267,000 metric tonnes of CO2 (2019 est.)",
                    "caption": "7.893 million metric tonnes of CO2 (2019 est.)"}
        assert expected == destructuring.destructure_list_like_with_caption(test_case_1)


test_case_3 = '''
<p>
    <strong>
    Fitch rating: 
    </strong>
    B (2018)
    <br>
    <br>
    <strong>Moody's rating: </strong>
    B3 (2018)
    <br>
    <br>
    <strong>Standard &amp; Poors rating: </strong>
    B (2017)
    <br>
    <br>
    <strong>note: </strong>
    The year refers to the year in which the current credit rating was first obtained.
</p>
'''

class TestDestructureListLikeParagraphWithNote:

    # This will not be probably different from the first case
    def test_for_destructure(self):

        expected = {"Fitch rating": "B (2018)",
                    "Moody's rating": "B3 (2018)",
                    "Standard &amp; Poors rating": "B (2017)",
                    "note": "The year refers to the year in which the current credit rating was first obtained."}
        assert expected == destructuring.destructure_list_like_with_note(test_case_1)


test_case_4 = '''
<p>
7.8% of GDP (2020)
</p>
'''


class TestDestructureParagraph:

    def test_for_destructure(self):

        expected = ["7.8% of GDP (2020)"]
        assert expected == destructuring.destructure_text_paragraph(test_case_1)


