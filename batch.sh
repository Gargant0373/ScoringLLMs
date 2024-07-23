#!/bin/sh

# # Ratings from -5 to 5 
# python src/ratings-5_5.py llama3
# python src/ratings-5_5.py dolphin-llama3
# python src/ratings-5_5.py mistral
# python src/ratings-5_5.py mixtral
#
# # Ratings -100 to 100
# python src/ratings-100_100.py llama3
# python src/ratings-100_100.py dolphin-llama3
# python src/ratings-100_100.py mistral
# python src/ratings-100_100.py mixtral
#
# # Ratings from 0 to 5
# python src/ratings-0_5.py llama3
# python src/ratings-0_5.py dolphin-llama3
# python src/ratings-0_5.py mistral
# python src/ratings-0_5.py mixtral

# python src/ratings.py llama3 0 10
# python src/ratings.py dolphin-llama3 0 10
# python src/ratings.py mistral 0 10
python src/ratings.py phi3 0 10

# python src/ratings.py llama3 0 200
# python src/ratings.py dolphin-llama3 0 200
# python src/ratings.py mistral 0 200
python src/ratings.py phi3 0 200
