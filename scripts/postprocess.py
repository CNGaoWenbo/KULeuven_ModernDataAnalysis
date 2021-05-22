# -*- coding: utf-8 -*-
"""
Created on Sat May  8 16:30:59 2021

@author: jordan
"""
import pandas as pd

def writeTopicWords(path='../data/Topics_UN.csv',optimal_model=[]):
    # write the frequent words into the csv file
    import re
    with open(path,'w') as fw: # write the result to a csv 
        fw.write("topic_id,term0,term1,term2,term3,term4,term5,term6,term7,term8,term9"+"\n")
        for i in optimal_model.print_topics():
            r1 = re.findall(r"\w+",i[1])
            line=str(i[0])
            for item in r1:
                if not item.isdigit():
                    line=line+','+item
            fw.write(line+'\n')
            
def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, proportion Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


def wordCloud(optimal_model,corpus,dictionary):

    # Wordcloud of Top N words in each topic
    #!pip install wordcloud
    from matplotlib import pyplot as plt
    from wordcloud import WordCloud, STOPWORDS
    import matplotlib.colors as mcolors
    
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'
    stopwords = set(STOPWORDS)
    
    cloud = WordCloud(
                      background_color='white',
                      stopwords=stopwords,
                      width=2500,
                      height=1800,
                      max_words=10,
                      colormap='tab10',
                      color_func=lambda *args, **kwargs: cols[i],
                      prefer_horizontal=1.0)
    
    topics = optimal_model.show_topics(formatted=False)
    
    fig, axes = plt.subplots(3, 3, figsize=(16,16), sharex=True, sharey=True)
    
    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
        plt.gca().axis('off')
    
    
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    plt.show()