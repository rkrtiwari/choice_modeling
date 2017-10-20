# Load the approprioate libraries
library(mlogit)

egress_choice <- read.csv("r_input_data.csv")

#########################################################################################################################
#BUS + MRT + TAXI combined
##########################################################################################################################
EC1 <- mlogit.data(egress_choice, shape="long", choice="decision", alt.var="alt")
res1<-mlogit(decision ~ dwell_time + incentive + waiting_time + congestion, data=EC)
summary(res1)

