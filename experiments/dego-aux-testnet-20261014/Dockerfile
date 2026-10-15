FROM public.ecr.aws/ubuntu/ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake ninja-build git ca-certificates python3 libboost-dev libboost-serialization-dev libcrypto++-dev libcxxopts-dev libminiupnpc-dev libssl-dev rapidjson-dev librocksdb-dev libcpp-httplib-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /research
