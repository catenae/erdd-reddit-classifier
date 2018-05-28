#!/bin/bash

LINKS_PATH=/opt/reddit-depression/erdd
cd $LINKS_PATH

case "$1" in
    text_vectorizer)
        LINK=text_vectorizer.py
        ;;

    vector_aggregator)
        LINK=vector_aggregator.py
        ;;

    tfidf_transformer)
        LINK=tfidf_transformer.py
        ;;

    model_predictor)
        LINK=model_predictor.py
        ;;

    post_updater)
        LINK=post_updater.py
        ;;

    alert_manager)
        LINK=alert_manager.py
        ;;

    alert_storer)
        LINK=alert_storer.py
        ;;

    probability_storer)
        LINK=probability_storer.py
        ;;

    *)
        echo "Usage: [text_vectorizer | vector_aggregator | tfidf_transformer |"
        echo "        model_predictor | post_updater | alert_manager |"
        echo "        probability_storer | alert_storer] [ARGS]"
        exit 1
esac

shift
python $LINK "$@"
