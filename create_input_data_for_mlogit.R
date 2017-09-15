# Load the approprioate libraries
library(mlogit)

# Change to appropriate directory
getwd()
setwd('C:\\Users\\tiwarir\\Documents\\behavior_learning\\r_codes')




###########################################################################
# create user choices
##########################################################################
choices_user_wants_to_leave <- function(df_s){
  individual = rep(df_s$user,6)
  gender = rep(df_s$gender,6)
  decision <- c(1,0,1,0,1,0)
  DT <- c(0,30,0,30,0,30)
  incentive <- c(0,0,0,5,0,10)
  mode <- rep(c('leave', 'stay'), 3)
  df_c <- data.frame(individual, decision, DT, incentive, gender, mode)
}


choices_user_wants_to_stay <- function(df_s){
  individual = rep(df_s$user,2)
  gender = rep(df_s$gender,2)
  decision <- c(0,1,0,1,0,1)
  DT <- c(0,df_s$dwell_time[1],0,df_s$dwell_time[2],0,df_s$dwell_time[3])
  incentive <- c(0,0,0,5,0,10)
  mode <- rep(c('leave', 'stay'), 3)
  df_c <- data.frame(individual, decision, DT, incentive, gender, mode)
}

choices_user_wants_to_stay_for_5 <- function(df_s){
  individual = rep(df_s$user,3)
  gender = rep(df_s$gender,3)
  decision <- c(1,0,0,1,0,1)
  DT <- c(0,df_s$dwell_time[1],0,df_s$dwell_time[1],0,df_s$dwell_time[2])
  incentive <- c(0,0,0,5,0,10)
  mode <- rep(c('leave', 'stay'), 3)
  df_c <- data.frame(individual, decision, DT, incentive, gender, mode)
}

choices_user_wants_to_stay_for_10 <- function(df_s){
  individual = rep(df_s$user,6)
  gender = rep(df_s$gender,6)
  decision <- c(1,0,1,0,0,1)
  DT <- c(0,df_s$dwell_time[1],0,df_s$dwell_time[1],0,df_s$dwell_time[1])
  incentive <- c(0,0,0,5,0,10)
  mode <- rep(c('leave', 'stay'), 3)
  df_c <- data.frame(individual, decision, DT, incentive, gender, mode)
}


###############################################################################
# determine user choices from the choice data
################################################################################
get_user_choice <- function(user){
  
  ind = choice_data$user == user
  df_s = choice_data[ind,]
  n_row = nrow(df_s)
  
  if (n_row == 1){
    if(df_s$incentive == 10){   
      df_c = choices_user_wants_to_stay_for_10(df_s)
    } else {                   
      df_c = choices_user_wants_to_leave(df_s)
    }
  }
  
  if (n_row  == 2){
    df_c = choices_user_wants_to_stay_for_5(df_s)
  }
  
  if (n_row == 3){ 
    df_c = choices_user_wants_to_stay(df_s)
  }
  return(df_c)
}

########################################################################
# create choice df
########################################################################
create_choice_df <- function(choice_data){
  users = unique(choice_data$user)
  df = data.frame(individual = integer(), decision = integer(), DT = integer(), incentive = integer(), gender = integer(), mode = character())
  for (user in users){
    df_c = get_user_choice(user)
    df = rbind(df, df_c)
  }
  return(df)  
}


########################################################################################
# create the input data
########################################################################################
choice_data = read.csv('..\\python_code\\choice_data.csv', header = TRUE)

df = create_choice_df(choice_data)
n_choice = nrow(df)/2
df$id = rep(1:n_choice, each = 2)

######################################################################################
# make the model
######################################################################################
Tr = mlogit.data(df, shape = 'long', choice = 'decision', varying = c('incentive', 'DT'), chid.var = 'id', alt.var = 'mode')
model <- mlogit(decision ~ incentive + DT, Tr)


#####################################################################################
# separate model for male and female
#####################################################################################
# Gender 1 (Male)
index_1 = df$gender == 1
df_1 = df[index_1,]
Tr_1 = mlogit.data(df_1, shape = 'long', choice = 'decision', varying = c('incentive', 'DT'), chid.var = 'id', alt.var = 'mode')
model_1 = mlogit(decision ~ incentive + DT | 0, Tr_1)

# Gender 2 (Female)
index_2 = df$gender == 2
df_2 = df[index_2,]
Tr_2 = mlogit.data(df_2, shape = 'long', choice = 'decision', varying = c('incentive', 'DT'), chid.var = 'id', alt.var = 'mode')
model_2 = mlogit(decision ~ incentive + DT |0, Tr_2)

# model coefficients
model_1$coefficients
model_2$coefficients


















