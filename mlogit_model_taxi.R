# Load the approprioate libraries
library(mlogit)

# Change to appropriate directory
getwd()
setwd('C:\\Users\\tiwarir\\Documents\\behavior_learning\\final_code')


#1. Taxi Congestion level 2
taxi_congestion_level_2 = read.csv('r_input_data_taxi_congestion_level_2.csv', header = TRUE)
n_choice_cong_2 = nrow(taxi_congestion_level_2)/2
taxi_congestion_level_2$id = rep(1:n_choice_cong_2, each = 2)
head(taxi_congestion_level_2)

#1. Taxi Congestion level 1
taxi_congestion_level_1 = read.csv('r_input_data_taxi_congestion_level_1.csv', header = TRUE)
n_choice_cong_1 = nrow(taxi_congestion_level_1)/2
taxi_congestion_level_1$id = rep((n_choice_cong_2 +1) :(n_choice_cong_1 + n_choice_cong_2), each = 2)
head(taxi_congestion_level_1)

# join the congestion level 1 and 2 together
taxi = rbind(taxi_congestion_level_2, taxi_congestion_level_1)
head(taxi)
tail(taxi)

#####################################################################################
# separate model for male and female
#####################################################################################
# Gender 1 (Male)
index_1 = taxi$gender == 1
df_1 = taxi[index_1,]
Tr_1 = mlogit.data(df_1, shape = 'long', choice = 'decision', varying = c('DT', 'WT', 'incentive'), chid.var = 'id', alt.var = 'mode')
model_1 = mlogit(decision ~ DT + WT + incentive | 0, Tr_1)

# Gender 2 (Female)
index_2 = taxi$gender == 2
df_2 = taxi[index_2,]
Tr_2 = mlogit.data(df_2, shape = 'long', choice = 'decision', varying = c('DT', 'WT', 'incentive'), chid.var = 'id', alt.var = 'mode')
model_2 = mlogit(decision ~ DT + WT + incentive |0, Tr_2)
sink("taxi_result.txt")
cat('_________________________________________________________________________________________________________')
cat('\nResult for Male\n')
cat('_________________________________________________________________________________________________________')
summary(model_1)
cat('_________________________________________________________________________________________________________')
cat('\nResult for female\n')
cat('_________________________________________________________________________________________________________')
summary(model_2)
sink()