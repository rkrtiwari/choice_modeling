library(mlogit)
setwd('C:\\Users\\tiwarir\\Documents\\behavior_learning\\scc_model')
egress_choice <- read.csv("r_input_data.csv")

#head(egress_choice, n)

EC <- mlogit.data(egress_choice, shape="long", choice="decision", alt.var="alt")

#head(EC)

res1<-mlogit(decision ~ dwell_time + incentive + congestion, data=EC)
summary(res1)