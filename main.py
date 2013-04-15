# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from corpus import *
from spec_analyser import *
from csv_to_html import *
from clips_facts_generation import ClipsFactsGeneration
from range_estimator import RangeCalculator
#from fuzzy_plot import *
#from scatter_plot import *
from dom import DegreeOfMembership
from neuro_fuzzy import NeuroFuzzySystem
#from neuron import *
#from surface_plot import *
from sect_clustering import SectionWiseClustering
import csv
import sys
import os

if __name__ == '__main__':
    spec_count = 0
    spec_word_count_list, corpus_words = [], []
    spec_bi_gram_count_list, corpus_bi_grams = [], []
    spec_tri_gram_count_list, corpus_tri_grams = [], []
    spec_four_gram_count_list, corpus_four_grams = [], []
    spec_five_gram_count_list, corpus_five_grams = [], []

    for root, directory, files in os.walk('./corpus'):
        for f in files:
            if f.endswith('.xml'):
                path = os.path.join(root, f)
                spec_words = []
                bi_grams = []
                tri_grams = []
                four_grams = []
                five_grams = []
                
                cor = Corpus(path, spec_words, bi_grams, tri_grams, four_grams, five_grams)
                cor.generateLocationVector(cor.parseXML(), [0])
                spec_count += 1
                
                spec_word_count = len(spec_words)
                spec_word_count_list.append(spec_word_count)
                corpus_words.append(spec_words)
                
                spec_bi_gram_count = len(bi_grams)
                spec_bi_gram_count_list.append(spec_bi_gram_count)
                corpus_bi_grams.append(bi_grams)

                spec_tri_gram_count = len(tri_grams)
                spec_tri_gram_count_list.append(spec_tri_gram_count)
                corpus_tri_grams.append(tri_grams)

                spec_four_gram_count = len(four_grams)
                spec_four_gram_count_list.append(spec_four_gram_count)
                corpus_four_grams.append(four_grams)

                spec_five_gram_count = len(five_grams)
                spec_five_gram_count_list.append(spec_five_gram_count)
                corpus_five_grams.append(five_grams)                

    corpus = []
    for spec in corpus_words:
        for word in spec:
            corpus.append(word)

    corpus_bigrams = []
    for spec in corpus_bi_grams:
        for word in spec:
            corpus_bigrams.append(word)

    corpus_trigrams = []
    for spec in corpus_tri_grams:
        for word in spec:
            corpus_trigrams.append(word)

    corpus_fourgrams = []
    for spec in corpus_four_grams:
        for word in spec:
            corpus_fourgrams.append(word)

    corpus_fivegrams = []
    for spec in corpus_five_grams:
        for word in spec:
            corpus_fivegrams.append(word)

    output = open('output_table.csv', 'wb')
    output_write = csv.writer(output)
    output_write.writerow(['S.No', 'Word', 'Location Vector', 'Signature', 'Signature Weight', 'Tf', 'Idf', 'Tf - Idf Score', 'English Dictionary Match', 'Number Match', 'Abbreviation Match', 'Symbol Match', 'Repetitive Word'])
    
    output_bigrams = open('output_table_bigrams.csv', 'wb')
    output_bigrams_write = csv.writer(output_bigrams)
    output_bigrams_write.writerow(['S.No', 'Bigram', 'Location Vector', 'Signature', 'Signature Weight', 'Tf', 'Idf', 'Tf - Idf Score', 'Is First Letter Capitalized', 'POS'])
    
    output_trigrams = open('output_table_trigrams.csv', 'wb')
    output_trigrams_write = csv.writer(output_trigrams)
    output_trigrams_write.writerow(['S.No', 'Trigram', 'Location Vector', 'Signature', 'Signature Weight', 'Tf', 'Idf', 'Tf - Idf Score', 'Is First Letter Capitalized', 'POS'])
    
    output_fourgrams = open('output_table_fourgrams.csv', 'wb')
    output_fourgrams_write = csv.writer(output_fourgrams)
    output_fourgrams_write.writerow(['S.No', 'Fourgram', 'Location Vector', 'Signature', 'Signature Weight', 'Tf', 'Idf', 'Tf - Idf Score', 'Is First Letter Capitalized', 'POS'])
    
    output_fivegrams = open('output_table_fivegrams.csv', 'wb')
    output_fivegrams_write = csv.writer(output_fivegrams)
    output_fivegrams_write.writerow(['S.No', 'Fivegram', 'Location Vector', 'Signature', 'Signature Weight', 'Tf', 'Idf', 'Tf - Idf Score', 'Is First Letter Capitalized', 'POS'])
    
    candidates = open('candidates.csv','wb')
    candidates_write = csv.writer(candidates)
    candidates_write.writerow(['S.No', 'Word', 'Location Vector', 'Signature', 'Tf', 'Idf', 'Tf - Idf Score'])

    spec_ID = 0
    path = sys.argv[1]
    spec_words = []
    bi_grams = []
    tri_grams = []
    four_grams = []
    five_grams = []

    loc_vec = LocationVector(path, spec_words, bi_grams, tri_grams, four_grams, five_grams)
    loc_vec.generateLocationVector(loc_vec.parseXML(), [0])

    spec_ID += 1
    statement_facts_data = []

    tagger = WordTagger(spec_ID, path, output_write, output_bigrams_write, output_trigrams_write, output_fourgrams_write, output_fivegrams_write, candidates_write, spec_words, bi_grams, tri_grams, four_grams, five_grams, statement_facts_data, corpus, corpus_bigrams, corpus_trigrams, corpus_fourgrams, corpus_fivegrams, spec_count, spec_word_count_list, spec_bi_gram_count_list, spec_tri_gram_count_list, spec_four_gram_count_list, spec_five_gram_count_list)
    tagger.generateLocationVector(tagger.parseXML(), [0])
    #tagger.printPercentageMatch()
    #tagger.accuracy()

    output.close()
    output_bigrams.close()
    output_trigrams.close()
    output_fourgrams.close()
    output_fivegrams.close()
    candidates.close()

    # ------------- printing out CLIPS facts ------------

    word_facts_list = tagger.word_facts_data
    statement_facts_list = tagger.statement_facts_data
    facts_gen = ClipsFactsGeneration()
    #facts_gen.generateWordFacts(word_facts_list)
    #facts_gen.generateSentenceFacts(statement_facts_list)

    # ------------- Word Bags ------------

    # tfidf info list of N-grams
    tf_idf_list = tagger.tf_idf_list  # all spec words (unique)
    tf_idf_bigram_list = tagger.tf_idf_bigram_list
    tf_idf_trigram_list = tagger.tf_idf_trigram_list
    tf_idf_fourgram_list = tagger.tf_idf_fourgram_list
    tf_idf_fivegram_list = tagger.tf_idf_fivegram_list

    # word bags Unigrams
    tf_idf_common_eng_words = tagger.common_eng_words  # common english excluding stopwords and words whose IDF = 1
    tf_idf_nouns_unigrams = tagger.nouns_unigrams  # uni-gram nouns excluding stopwords and words whose IDF = 1
    tf_idf_loc_sig_link = tagger.loc_sig_link_unigrams  # uni-grams whose location signature is "Link"

    # ------------ word bags Bigrams -----------

    tf_idf_bigram_NNP_NNP = tagger.bigram_NNP_NNP  # bi-grams with NNP + NNP POS
    tf_idf_bigram_NNP_NN = tagger.bigram_NNP_NN  # bi-grams with NNP + NN POS
    tf_idf_bigram_NN_NN = tagger.bigram_NN_NN  # bi-grams with NN + NN POS

    # ------------ word bags Trigrams -----------

    tf_idf_trigram_NNP_NNP_NNP = tagger.trigram_NNP_NNP_NNP  # tri-grams with NNP + NNP + NNP POS
    tf_idf_trigram_NNP_NNP_NN = tagger.trigram_NNP_NNP_NN  # tri-grams with NNP + NNP + NN POS
    tf_idf_trigram_NNP_NN_NN = tagger.trigram_NNP_NN_NN  # tri-grams with NNP + NN + NN POS
    tf_idf_trigram_NN_NN_NN = tagger.trigram_NN_NN_NN  # tri-grams with NN + NN + NN POS

    # ------------ word bags Fourgrams -----------

    tf_idf_fourgram_NNP_NNP_NNP_NNP = tagger.fourgram_NNP_NNP_NNP_NNP  # fourgrams with NNP + NNP + NNP + NNP POS

    # ------------ word bags Fivegrams -----------
    tf_idf_fivegram_NNP_NNP_NNP_NNP_NNP = tagger.fivegram_NNP_NNP_NNP_NNP_NNP  # fivegrams with NNP + NNP + NNP + NNP + NNP POS

    def neuro_fuzzy(x):
        range_span = RangeCalculator()
        range_span.calculateFilterIRange(x)
        #tf_idf_values = range_span.tf_idf_values
        span = range_span.span
        span_pivots = range_span.pivots

        # ------------- Drawing Fuzzy & Scatter Plots --------------

        #draw_fuzzy = FuzzyPlotFilterI()
        #draw_fuzzy.drawFuzzyPlotFilterI(tf_idf_values, span)
        #draw_scatter = ScatterPlot()
        #draw_scatter.drawScatterPlot(tf_idf_values)

        # ------------- calculating DOM of fuzzy sets --------------

        dom = DegreeOfMembership()
        dom.findFuzzySet(x, span, span_pivots)
        y = dom.dom_data_list
        return y

        # ----------------------------------------------------------

    u1 = neuro_fuzzy(tf_idf_common_eng_words)
    u2 = neuro_fuzzy(tf_idf_nouns_unigrams)
    u3 = neuro_fuzzy(tf_idf_loc_sig_link)

    # feature set for bigrams
    b1 = neuro_fuzzy(tf_idf_bigram_NNP_NNP)
    b2 = neuro_fuzzy(tf_idf_bigram_NNP_NN)
    b3 = neuro_fuzzy(tf_idf_bigram_NN_NN)

    # feature set for trigrams
    t1 = neuro_fuzzy(tf_idf_trigram_NNP_NNP_NNP)
    t2 = neuro_fuzzy(tf_idf_trigram_NNP_NNP_NN)
    t3 = neuro_fuzzy(tf_idf_trigram_NNP_NN_NN)
    t4 = neuro_fuzzy(tf_idf_trigram_NN_NN_NN)

    # feature set for fourgrams
    f1 = neuro_fuzzy(tf_idf_fourgram_NNP_NNP_NNP_NNP)

    # feature set for fivegrams
    p1 = neuro_fuzzy(tf_idf_fivegram_NNP_NNP_NNP_NNP_NNP)  # p --> penta = five

    nf = NeuroFuzzySystem()
    nf.neuroFuzzyModelling(tf_idf_list, u1, u2, u3, tf_idf_bigram_list, b1, b2, b3, tf_idf_trigram_list, t1, t2, t3, tf_idf_fourgram_list, f1, tf_idf_fivegram_list, p1)

    nf.normCOGUnigrams()
    nf.normCOGBigrams()
    nf.normCOGTrigrams()
    nf.normCOGFourgrams()
    nf.normCOGFivegrams()

    PI_bundle_unigrams = NeuroFuzzySystem.PI_bundle_unigrams

    section_bundle = tagger.sections

    sec = SectionWiseClustering(PI_bundle_unigrams, section_bundle)
    sec.findSectionHeaders()
    sec.clusterWordsBySection()



    #cog_list = nf.cog_list
    #surface = SurfacePlotCOG()
    #surface.drawSurfacePlot(cog_list)

    # ------------------- letting NN do it's job --------------------
    #nn = NeuralNetwork(tf_idf_list, f1, f2, f3)
    #nn.trainNN()
    # ---------------------------------------------------------------

    output_csv = csv.reader(open('output_table.csv', 'rb'))
    output_html = open('output_table.html', 'w')
    html = CsvToHtml()
    html.htmlOutputTable(output_csv, output_html)
    
    output_bigrams_csv = csv.reader(open('output_table_bigrams.csv', 'rb'))
    output_bigrams_html = open('output_table_bigrams.html', 'w')
    html.htmlOutputTable(output_bigrams_csv, output_bigrams_html)

    output_trigrams_csv = csv.reader(open('output_table_trigrams.csv', 'rb'))
    output_trigrams_html = open('output_table_trigrams.html', 'w')
    html.htmlOutputTable(output_trigrams_csv, output_trigrams_html)

    output_fourgrams_csv = csv.reader(open('output_table_fourgrams.csv', 'rb'))
    output_fourgrams_html = open('output_table_fourgrams.html', 'w')
    html.htmlOutputTable(output_fourgrams_csv, output_fourgrams_html)

    output_fivegrams_csv = csv.reader(open('output_table_fivegrams.csv', 'rb'))
    output_fivegrams_html = open('output_table_fivegrams.html', 'w')
    html.htmlOutputTable(output_fivegrams_csv, output_fivegrams_html)

    candidates_csv = csv.reader(open('candidates.csv', 'rb'))
    candidates_html = open('candidates.html', 'w')
    html.htmlOutputTable(candidates_csv, candidates_html)