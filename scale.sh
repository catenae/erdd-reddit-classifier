#!/bin/bash

./build.sh

NUMBER=${2:-9}
CPUS=${1:-0-3}

TS=$(date +%s)
for i in $(seq 1 $NUMBER); do
  TS=$((TS + 1))

  docker run -d --restart unless-stopped --net=host --name text_vectorizer_$TS \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links text_vectorizer \
  -i new_texts \
  -o count_vectors \
  -b localhost:9092 \
  -a localhost:3000 \
  -p aerospike:test:setup_objects &
  docker run -d --restart unless-stopped --net=host --name text_vectorizer_${TS}_1 \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links text_vectorizer \
  -i new_texts \
  -o count_vectors \
  -b localhost:9092 \
  -a localhost:3000 \
  -p aerospike:test:setup_objects &


  docker run -d --restart unless-stopped --net=host --name tfidf_transformer_$TS \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links tfidf_transformer \
  -i count_vectors,aggregated_vectors \
  -o tfidf_vectors \
  -b localhost:9092 \
  -a localhost:3000 \
  -p aerospike:test:setup_objects &
  docker run -d --restart unless-stopped --net=host --name tfidf_transformer_${TS}_1 \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links tfidf_transformer \
  -i count_vectors,aggregated_vectors \
  -o tfidf_vectors \
  -b localhost:9092 \
  -a localhost:3000 \
  -p aerospike:test:setup_objects &
  docker run -d --restart unless-stopped --net=host --name tfidf_transformer_${TS}_2 \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links tfidf_transformer \
  -i count_vectors,aggregated_vectors \
  -o tfidf_vectors \
  -b localhost:9092 \
  -a localhost:3000 \
  -p aerospike:test:setup_objects &
  docker run -d --restart unless-stopped --net=host --name tfidf_transformer_${TS}_3 \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links tfidf_transformer \
  -i count_vectors,aggregated_vectors \
  -o tfidf_vectors \
  -b localhost:9092 \
  -a localhost:3000 \
  -p aerospike:test:setup_objects &

  docker run -d --restart unless-stopped --net=host --name vector_aggregator_$TS \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links vector_aggregator \
  -i count_vectors \
  -o aggregated_vectors \
  -b localhost:9092 \
  -a localhost:3000 &
  docker run -d --restart unless-stopped --net=host --name vector_aggregator_${TS}_1 \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links vector_aggregator \
  -i count_vectors \
  -o aggregated_vectors \
  -b localhost:9092 \
  -a localhost:3000 &
  docker run -d --restart unless-stopped --net=host --name vector_aggregator_${TS}_2 \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links vector_aggregator \
  -i count_vectors \
  -o aggregated_vectors \
  -b localhost:9092 \
  -a localhost:3000 &
  docker run -d --restart unless-stopped --net=host --name vector_aggregator_${TS}_3 \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links vector_aggregator \
  -i count_vectors \
  -o aggregated_vectors \
  -b localhost:9092 \
  -a localhost:3000 &

  docker run -d --restart unless-stopped --net=host --name model_predictor_$TS \
  --cpuset-cpus="$CPUS" \
  catenae/erdd-links model_predictor \
  -i tfidf_vectors \
  -o user_probabilities,text_probabilities,processed_users,processed_texts \
  -b localhost:9092 \
  -a localhost:3000 \
  -p aerospike:test:setup_objects &

done

wait
